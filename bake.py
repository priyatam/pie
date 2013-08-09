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
import time
from datetime import datetime
import imp
import json
import os
import yaml
import markdown as md
import pystache
import scss
import coffeescript
import cssmin
import jsmin
import argparse
from subprocess import Popen, PIPE
from codecs import open


### API ###

def load_config(config_path):
    """Loads configuration from config.yaml"""
    with open(config_path, "r", "utf-8") as fin:
        return yaml.load(fin.read())


def load_contents(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    contents = []
    for fname in os.listdir(config['content']):
        if fname.endswith('.md') or fname.endswith('.txt'):
            try:
                yaml_data, raw_data = _read_yaml(config['content'], fname)
                fname = config['content'] + os.sep + fname
                content = {
                    "name": os.path.basename(fname),
                    "body": raw_data, # unprocessed
                    "modified_date": _format_date(fname)
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
    modules = [imp.load_source("lambda" + recipe, config['lambdas'] + os.sep + recipe + ".py") for recipe in _get_lambdas(config)]
    return {funcname: getattr(mod, funcname) for mod in modules for funcname in dir(mod) if not funcname.startswith("__")}


def compile_asset(config, asset_type, fname):
    """Closure: Compiles asset types: css, js, html using pre-processors"""
    def _compile(__compile, _from, _to, ):
        raw_data = __compile(config)
        # Avoid including the output twice. Hint bake, by adding a _ filename convention
        new_filename = "_" + fname.replace(_from, _to)
        open(config[asset_type] + os.sep + new_filename, 'w', "utf-8").write(raw_data)
        return raw_data
    return _compile


def load_recipes(config):
    """Pre-process and load each asset type into a dict and return as a single recipe package: a tuple of dicts"""

    # Compile CSS
    style = None
    scss_file_name = config["styles"] + "/style.scss"
    if os.path.isfile(scss_file_name):
        style = compile_asset(config, "styles", "style.scss")(_compile_scss, 'scss', 'css')
    else:
        style = _read("style.css", config["styles"])

    # Compile Coffeescript
    script = None
    cs_file_name = config["scripts"] + os.sep + "/script.coffee"
    if os.path.isfile(cs_file_name):
        script = compile_asset(config, "scripts", "script.coffee")(_compile_scss, 'coffee', 'js')
    else:
        script = _read("script.js", config["scripts"])

    # Load 3rd party logic
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

    renderer = pystache.Renderer(search_dirs=[config["templates"]], file_encoding="utf-8", string_encoding="utf-8", escape=lambda u: u)
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

def _get_template_path(config, name):
    return config["templates"] + os.sep + name


def _read(fname, subdir):
    """Reads subdir/fname as raw content"""
    with open(subdir + os.sep + fname, "r", "utf-8") as fin:
        return fin.read()


def _read_yaml(subdir, fname):
    """Splits subdir/fname into a tuple of YAML and raw content"""
    with open(subdir + os.sep + fname, "r", "utf-8") as fin:
        yaml_and_raw = fin.read().split('\n---\n')
        if len(yaml_and_raw) == 1:
            return {}, yaml_and_raw[0]
        else:
            return yaml.load(yaml_and_raw[0]), yaml_and_raw[1]


def _serve_github(config):
    """TODO: Refactor this from brute force to git api"""
    proc = Popen(['git', 'config', "--get", "remote.origin.url"], stdout=PIPE)
    url = proc.stdout.readline().rstrip("\n")
    os.system("rm -rf .build")
    os.system("git clone -b gh-pages " + url + " .build")
    os.system("cp deploy/index.html .build/")
    os.system("cd .build; git add index.html; git commit -m 'new deploy " + datetime.now() + "'; git push --force origin gh-pages")


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
    _params = __newdict(post, {'body': html_md})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["templates"]], file_encoding="utf-8", string_encoding="utf-8", escape= lambda u: u)
    return renderer.render_path(_get_template_path(config, template_name), _params)


def _textstache(config, content, template_name, lambdas=None):
    """Converts Markdown/Mustache/YAML to HTML."""
    txt = content['body']
    _params = __newdict(content, {'body': txt})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["templates"]], file_encoding="utf-8", string_encoding="utf-8", escape=lambda u: u)
    return renderer.render_path(_get_template_path(config, template_name), _params)


def _compile_scss(config):
    _scss = scss.Scss(scss_opts={"compress": False, "load_paths": [config["styles"]]})
    return _scss.compile(_read("style.scss", config["styles"]))


def _compile_coffee(asset_type, fname):
    return coffeescript.compile(_read(fname, asset_type))


def _format_date(fname):
    return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def _get_lambdas(config):
    return [f.strip('.py') for f in os.listdir(config['lambdas']) if f.endswith('py') and not f.startswith("__")]


def __newdict(*dicts):
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict


### MAIN ###

def main(config, to_serve=False):
    """Let's cook an Apple Pie"""
    contents = load_contents(config)
    style, script, lambdas = load_recipes(config)

    pie = bake(config, contents, style, script, lambdas, minify=to_serve)
    open('deploy/index.html', 'w', "utf-8").write(pie)
    print 'Generated index.html'

    if to_serve:
        serve(config)


if __name__ == '__main__':
    # Parse commmand line options
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="*", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yaml"])
    parser.add_argument("--recipe", nargs=1, default=["recipe"])
    args = parser.parse_args(sys.argv[1:])
    config_path = args.config[0]
    print "Using config from " + config_path
    _config = load_config(config_path)

    # This way, the user can do --recipe=default and expect it to work
    if args.recipe[0] != "recipe":
        _download_recipe(_config, args.recipe[0])

    to_serve = False
    if "serve" in args.string_options:
        to_serve = True

    main(_config, to_serve=to_serve)
