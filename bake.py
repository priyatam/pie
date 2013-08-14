#!/usr/bin/env python
"""
Usage:
./bake.py

To serve in gh-pages
./bake.py serve

Algo:
Read config.yaml. For each post.md, process YAML, and apply its Mustache Templates, and generate final HTML.
Lastly, combine everything into a single index.html with a minified CSS, JS.
"""

import sys
from datetime import datetime
import imp
import json
import os
import markdown as md
import pystache
import scss
import coffeescript
import cssmin
import jsmin
import argparse
from subprocess import Popen, PIPE
from codecs import open
from pieutils import *


### API ###

def load_contents(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    contents = []
    content_path = config['content']
    for fname in os.listdir(content_path):
        if fname.endswith('.md') or fname.endswith('.txt'):
            try:
                yaml_data, raw_data = read_yaml(content_path, fname)
                fname = content_path + os.sep + fname
                content = {
                    "name": os.path.basename(fname),
                    "body": raw_data,  # unprocessed
                    "modified_date": format_date(fname)
                }
                content.update(yaml_data)  # Merge Yaml data for future lookup
                contents.append(content)
            except:
                print "Error occured reading file: %s, " % fname
        else:
            print "Warning: Incorrect Extension"
    return contents


def load_lambdas(config):
    """Loads all pure functions from each module under 'lambdas' as a dictionary lookup by funcion name"""
    # recipe should be foo.bar.baz, not .foo.bar.baz or ..foo.bar.baz or foo/bar/baz, hence the regex
    lambdas_path = config['recipe_root'] + os.sep + "lambdas"
    modules = [imp.load_source("lambda" + recipe, lambdas_path + os.sep + recipe + ".py") for recipe in _get_lambdas(config)]
    return {funcname: getattr(mod, funcname) for mod in modules for funcname in dir(mod) if not funcname.startswith("__")}


def compile_asset(config, subdir, fname):
    """Closure: Compiles asset types: css, js, html using pre-processors"""
    def _compile(__compile, _from, _to, ):
        raw_data = __compile(config)
        # Avoid including the output twice. Hint bake, by adding a _ filename convention
        new_filename = "_" + fname.replace(_from, _to)
        open(subdir + os.sep + new_filename, 'w', "utf-8").write(raw_data)
        return raw_data
    return _compile


def load_recipes(config):
    """Pre-process and load each asset type into a dict and return as a single recipe package: a tuple of dicts"""
    _styles_path = config["recipe_root"] + os.sep + "styles"
    scss_file_name = _styles_path + os.sep + "style.scss"
    if os.path.isfile(scss_file_name):
        style = compile_asset(config, _styles_path, "style.scss")(_compile_scss, 'scss', 'css')
    else:
        style = read("style.css", _styles_path)
    script = read("script.js", "lib")
    lambdas = load_lambdas(config)
    return style, script, lambdas


def bake(config, contents, style, script, lambdas, minify=False):
    """Parse everything. Wrap results in a single page of html, css, js
       NOTE: This function modifies 'contents' by adding a new contents['html'] element"""

    # Content
    processor = {".txt": _textstache, ".md": _markstache}
    for content in contents:
        try:
            for ext in processor.keys():
                if content['name'].endswith(ext):
                    _tmpl = content.get('template', config['default_template'])  # set default if no template assigned
                    content['html'] = processor[ext](config, content, _tmpl, lambdas)
        except RuntimeError as e:
            print "Error baking content: %s %s" % content, e

    _params = {"title": config['title']}

    # Script & Style
    if minify:
        _params.update({"style_sheet": cssmin.cssmin(style),
                        "script": jsmin.jsmin(script)})
    else:
        _params.update({"style_sheet": style,
                        "script": script})

    #Lambdas
    _params.update(lambdas)

    # Json Data
    _params.update({"config": config})
#    _params.update({"json_data": json.dumps(contents, indent=4, separators=(',', ': '))})
    _params.update({"json_data": json.dumps(contents)})

    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_get_template_path(config, "index.mustache"), _params)


def serve(config, version=None):
    __config_path = "config.github.yaml"
    try:
        with open(__config_path, "r", "utf-8"): pass
    except IOError:
        print 'You need a config.github.yaml for serve.'
        exit(1)

    # Currently supports github
    _serve_github(config)


### SPI ###

def _serve_github(config):
    """TODO: Refactor this from brute force to git api"""
    proc = Popen(['git', 'config', "--get", "remote.origin.url"], stdout=PIPE)
    url = proc.stdout.readline().rstrip("\n")
    os.system("mv .build/index.html deploy/")
    os.system("rm -rf .build")
    os.system("git clone -b gh-pages " + url + " .build")
    os.system("cp deploy/index.html .build/")
    os.system("cd .build; git add index.html; git commit -m 'new deploy " + str(datetime.now()) + "'; git push --force origin gh-pages")


def _download_recipe(config, name):
    """TODO: Refactor this from brute force to git api"""
    os.system("rm -rf .build")
    os.system("rm -rf recipe.old")
    os.system("git clone " + config["recipes_repo"] + " .build")
    os.system("mv recipe recipe.old")
    os.system("cp -R .build/" + name + " recipe")


def _markstache(config, post, template_name, lambdas=None):
    """Converts Markdown/Mustache/YAML to HTML."""
    html_md = md.markdown(post['body'])
    _params = newdict(post, {'body': html_md})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_get_template_path(config, template_name), _params)


def _textstache(config, content, template_name, lambdas=None):
    """Converts Markdown/Mustache/YAML to HTML."""
    txt = content['body']
    _params = newdict(content, {'body': txt})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8", escape=lambda u: u)
    return renderer.render_path(_get_template_path(config, template_name), _params)


def _compile_scss(config):
    _scss = scss.Scss(scss_opts={"compress": False, "load_paths": [config["recipe_root"] + os.sep + "styles"]})
    return _scss.compile(read("style.scss", config["recipe_root"] + os.sep + "styles"))


def _compile_coffee(config):
    return coffeescript.compile(read("script.coffee", config['recipe_root'] + os.sep + "scripts"))


def _get_lambdas(config):
    lambdas_path = config['recipe_root'] + os.sep + "lambdas"
    return [f.strip('.py') for f in os.listdir(lambdas_path) if f.endswith('py') and not f.startswith("__")]


def _get_template_path(config, name):
    return config["recipe_root"] + os.sep + "templates" + os.sep + name


def _parse_cmd_args(args):
    """Parses Cmd line args"""
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="*", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yaml"])
    parser.add_argument("--recipe", nargs=1, default=["recipe"])
    return parser.parse_args(args[1:])


### MAIN ###

def main(config, to_serve=False):
    """Let's cook an Apple Pie"""
    contents = load_contents(config)
    style, script, lambdas = load_recipes(config)
    pie = bake(config, contents, style, script, lambdas, minify=to_serve)

    os.system('mkdir .build') if not os.path.isdir(".build") else None
    open('.build/index.html', 'w', "utf-8").write(pie)
    print 'Generated .build/index.html'
    
    serve(config) if to_serve else 'Use bake serve to deploy the site to github'


if __name__ == '__main__':
    args = _parse_cmd_args(sys.argv)
    sys_config = load_config("config.yaml")
    user_config = load_config(args.config[0])
    _config = sys_config if not user_config else dict(sys_config, **user_config) # Merge    
    _download_recipe(_config, args.recipe[0]) if args.recipe[0] != "recipe" else 'Using default recipe'
    to_serve = True if "serve" in args.string_options else False
    main(_config, to_serve=to_serve)