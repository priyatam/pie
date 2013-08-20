#!/usr/bin/env python
"""
Usage:
./bake.py

To serve in gh-pages
./bake.py serve

Algo:
Read config.yml.
For each post.md, process YAML, and apply its Mustache Templates, and generate final HTML.
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
import logging, logging.config
from pieutils import *


### API ###

@analyze
def load_contents(config):
    """Create a dictionary for retrieving content's raw body, meta data, and compiled html"""
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
                content.update(yaml_data) # Merge yaml
                contents.append(content)
            except:
                logger.error("Error occured reading file: %s, " % fname)
        else:
            logger.warning("Incorrect Extension: %s" % fname)
    return contents


@analyze
def load_lambdas(config):
    """Load all pure functions from each module under 'lambdas' as a dictionary by funcion name"""
    # recipe should be foo.bar.baz, not .foo.bar.baz or ..foo.bar.baz or foo/bar/baz, hence the regex
    lambdas_path = config['recipe_root'] + os.sep + "lambdas"
    modules = [imp.load_source("lambda" + recipe, lambdas_path + os.sep + recipe + ".py") for recipe in _get_lambdas(config)]
    return {funcname: getattr(mod, funcname) for mod in modules for funcname in dir(mod) if not funcname.startswith("__")}


@analyze
def compile_asset(config, subdir, fname):
    """Compile asset types: css, js, html using pre-processors"""
    def _compile(__compile, _from, _to, ):
        raw_data = __compile(config)
        # Avoid including the output twice. Hint bake, by adding a _ filename convention
        new_filename = "_" + fname.replace(_from, _to)
        open(subdir + os.sep + new_filename, 'w', "utf-8").write(raw_data)
        return raw_data
    return _compile


@analyze
def load_recipes(config):
    """Create a tuple of dictionaries, each providing  access to compiled sytles, scripts, and raw lambdas (with dictionary data)"""
    _styles_path = config["recipe_root"] + os.sep + "styles"
    scss_file_name = _styles_path + os.sep + "style.scss"
    if os.path.isfile(scss_file_name):
        style = compile_asset(config, _styles_path, "style.scss")(_compile_scss, 'scss', 'css')
    else:
        style = read("style.css", _styles_path)
    script = read("script.js", "lib")
    lambdas = load_lambdas(config)
    return style, script, lambdas

@analyze
def bake(config, contents, style, script, lambdas, minify=False):
    """Bake everything into a single index.html containing styles and scripts and a json of config, metadata, and compiled html"""
    processor = {".txt": _textstache, ".md": _markstache}
    logger.info('Baking Text and Markdown contents into HTML')
    for content in contents:
        try:
            for ext in processor.keys():
                if content['name'].endswith(ext):
                    _tmpl = content.get('template', config['default_template'])
                    logger.debug('Found Template: %s for content: %s', _tmpl, content['name'])
                    content['html'] = processor[ext](config, content, _tmpl, lambdas)
        except RuntimeError as e:
            logger.error("Error baking content: %s %s" % content, e)

    _params = {"title": config['title']}

    logger.info('Baking Styles and Scripts')
    if minify:
        _params.update({"style_sheet": cssmin.cssmin(style), "script": jsmin.jsmin(script)})
    else:
        _params.update({"style_sheet": style, "script": script})

    logger.info('Baking Lambdas')
    _params.update(lambdas)

    logger.info('Baking Config')
    _params.update({"config": config})
    logger.info('Baking contents into json_data')
    _params.update({"json_data": json.dumps(contents)})
    logger.info('Generating root index.html using index.mustache')
    _index_page = _get_template_path(config, "index.mustache")
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_index_page, _params)


@analyze
def serve(config, directory_path, version=None):
    """Preparing to serve index.html to a hosting provider"""
    __config_path = "config.github.yml"
    try:
        with open(__config_path, "r", "utf-8"): pass
    except IOError:
        logger.error('You need a config.github.yml to serve.')
        exit(1)

    logger.info('Currently supports only gh-pages')
    _serve_github(config, directory_path)


### SPI ###

@analyze
def _serve_github(config, directory_path):
    """Serve baked index.html into gh-pages"""
    # TODO: Refactor this from brute force to git api
    proc = Popen(['git', 'config', "--get", "remote.origin.url"], stdout=PIPE)
    url = proc.stdout.readline().rstrip("\n")
    os.chdir(directory_path)
    os.system("mv .build/index.html deploy/")
    os.system("rm -rf .build")
    os.system("git clone -b gh-pages " + url + " .build")
    os.system("cp deploy/index.html .build/")
    os.system("cd .build; git add index.html; git commit -m 'new deploy " + str(datetime.now()) + "'; git push --force origin gh-pages")


def _download_recipe(config, name):
    """Download recipes from github repo"""
    # TODO: Refactor this from brute force to git api
    os.system("rm -rf .build")
    os.system("rm -rf recipe.old")
    os.system("git clone " + config["recipes_repo"] + " .build")
    os.system("mv recipe recipe.old")
    os.system("cp -R .build/" + name + " recipe")


@analyze
def _markstache(config, post, template_name, lambdas=None):
    """Convert Markdown-YAML from its Mustache Template into HTML"""
    _html = md.markdown(post['body'])
    _params = newdict(post, {'body': _html})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_get_template_path(config, template_name), _params)


@analyze
def _textstache(config, content, template_name, lambdas=None):
    """Convert PlainText-YAML from its Mustache Template into HTML"""
    txt = content['body']
    _params = newdict(content, {'body': txt})
    _params.update(lambdas) if lambdas else None
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_get_template_path(config, template_name), _params)


def _compile_scss(config):
    _styles_path = config["recipe_root"] + os.sep + "styles"
    _scss = scss.Scss(scss_opts={"compress": False, "load_paths": [_styles_path]})
    return _scss.compile(read("style.scss", _styles_path))


def _compile_coffee(config):
    return coffeescript.compile(read("script.coffee", config['recipe_root'] + os.sep + "scripts"))


def _get_lambdas(config):
    lambdas_path = config['recipe_root'] + os.sep + "lambdas"
    return [f.strip('.py') for f in os.listdir(lambdas_path) if f.endswith('py') and not f.startswith("__")]


def _get_template_path(config, name):
    return config["recipe_root"] + os.sep + "templates" + os.sep + name


@analyze
def _parse_cmd_args(args):
    """Parse command line args"""
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="*", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yml"])
    parser.add_argument("--recipe", nargs=1, default=["recipe"])
    #parser.add_argument("--log", nargs=1, default=["INFO"])
    return parser.parse_args(args[1:])


### MAIN ###

@analyze
def main():
    """Let's cook an Apple Pie:"""
    logger.info('Understanding config')
    args = _parse_cmd_args(sys.argv)
    sys_config = load_config("config.yml")
    config_path = args.config[0]
    user_config = load_config(config_path)
    config = sys_config if not user_config else dict(sys_config, **user_config) # Merge

    logger.info('Checking if Recipes are required')
    _download_recipe(_config, args.recipe[0]) if args.recipe[0] != "recipe" else logger.info('Using default recipe')

    to_serve = True if "serve" in args.string_options else False

    logger.info('Cooking now')
    contents = load_contents(config)
    style, script, lambdas = load_recipes(config)
    pie = bake(config, contents, style, script, lambdas, minify=to_serve)

    directory_path = os.path.dirname(os.path.realpath(config_path))
    os.chdir(directory_path)
    os.system('mkdir .build') if not os.path.isdir(".build") else None
    open('.build/index.html', 'w', "utf-8").write(pie)
    logger.info('Generated ' + directory_path + '/.build/index.html')

    logger.info('Ready to serve')
    serve(config, directory_path) if to_serve else logger.info('(Run bake serve to deploy the site to github)')


if __name__ == '__main__':
    logger = get_logger()
    logger.info('Starting ...')
    main()
    logger.info('Finished!')
