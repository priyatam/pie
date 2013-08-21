#!/usr/bin/env python
"""
    compile:
        bake.py
    compile-and-host-on-gh-pages:
        bake.py serve
    algo:
        Read config.yml.
        For each post.md, process YAML, and apply its Mustache Templates, and generate final HTML.
        Combine everything into a single index.html with a minified CSS, JS.
    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License, see LICENSE for more details
"""

import logging, logging.config
import sys
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
from datetime import datetime
from pieutils import *


### API ###

@analyze
def load_contents(config):
    """Create a dictionary for retrieving content's raw body, metadata, and future compiled html"""
    contents = []
    path = config['content']
    for fname in os.listdir(path):
        if fname.endswith('.md') or fname.endswith('.txt'):
            try:
                meta, raw = read_yaml(path, fname)
                content = {
                    "name": meta['type'] + "/" + fname,
                    "body": raw,
                    "modified_date": format_date(path + os.sep + fname)
                }
                content.update(meta)
                contents.append(content)
            except RuntimeError as e:
                logger.error("Error while reading content: %s:\n%s" % fname, e)
        else:
            logger.warning("Incorrect Extension: %s" % fname)
    return contents



@analyze
def load_dynamic_templates(config):
    """Create a dictionary for retrieving template's raw body, metadata,
    and compiled html"""
    templates = []
    path = config["recipe_root"] + os.sep + "templates"
    for fname in os.listdir(path):
        if fname.endswith('.mustache'):
            try:
                meta, raw = read_yaml(path, fname)
                if meta.get('type', 'simple') == 'dynamic':
                    template = {
                        "name": os.path.splitext(fname)[0],
                        "body": raw,
                        "modified_date": format_date(path + os.sep + fname)
                    }
                    template.update(meta)
                    templates.append(template)
            except RuntimeError as e:
                logger.error("Error while reading template: %s:\n%s" % fname, e)
        else:
            logger.warning("Incorrect Extension: %s" % fname)
    return templates


@analyze
def load_lambdas(config, contents, dynamic_templates):
    """Load all pure functions from each module under 'lambdas' as a dictionary by funcion name"""
    # recipe should be foo.bar.baz, not .foo.bar.baz or ..foo.bar.baz or foo/bar/baz
    lambdas_path = config['recipe_root'] + os.sep + "lambdas"
    modules = [imp.load_source(recipe, lambdas_path + os.sep + recipe + ".py") for recipe in _get_lambdas(config)]
    for module in modules:
        module.contents = contents
        module.dynamic_templates = dynamic_templates
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
def load_recipes(config, contents, dynamic_templates):
    """Create a tuple of dictionaries, each providing  access to compiled sytle, script, and raw lambdas (along with their dictionary data)"""
    _styles_path = config["recipe_root"] + os.sep + "styles"
    scss_file_name = _styles_path + os.sep + "style.scss"
    if os.path.isfile(scss_file_name):
        style = compile_asset(config, _styles_path, "style.scss")(_compile_scss, 'scss', 'css')
    else:
        style = read("style.css", _styles_path)
    script = read("script.js", "lib")
    lambdas = load_lambdas(config, contents, dynamic_templates)
    return style, script, lambdas


@analyze
def bake(config, contents, dynamic_templates, style, script, lambdas,
         minify=False):
    """Bake recipes with given style and script into a single index.html along with a json of style, script, and content"""
    params = {"title": config['title']}

    logger.info('Baking Contents and Dynamic Templates')
    bake_contents(config, contents, lambdas)
    bake_dynamic_templates(config, dynamic_templates, lambdas)
#    params.update({"json_data": json.dumps(contents + dynamic_templates, indent=5, separators=(',', ': '))})
    params.update({"json_data": json.dumps(contents + dynamic_templates)})

    logger.info('Baking Styles and Scripts')
    if minify:
        params.update({"style_sheet": cssmin.cssmin(style), "script": jsmin.jsmin(script)})
    else:
        params.update({"style_sheet": style, "script": script})

    logger.info('Baking Lambdas')
    params.update(lambdas)

    logger.info('Baking Config')
    params.update({"config": config})

    logger.info('Generating root index.html using index.mustache')
    _index_page = _get_template_path(config, "index.mustache")
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")

    return renderer.render_path(_index_page, params)


@analyze
def bake_contents(config, contents, lambdas):
    """Baking Contents into HTML using Mustache Templates"""
    logger.info('Baking Contents into HTML')
    for content in contents:
        try:
            if content['name'].endswith('.txt'):
                template = content.get('template', config['default_template'])
                logger.debug('Found Template: %s for content: %s', template, content['name'])
                content['html'] = _textstache(config, content, template, lambdas)
            elif content['name'].endswith('.md'):
                template = content.get('template', config['default_template'])
                logger.debug('Found Template: %s for content: %s', template, content['name'])
                content['html'] = _markstache(config, content, template, lambdas)
        except RuntimeError as e:
           logger.error("Error Baking Contents: %s" % content, e)


@analyze
def bake_dynamic_templates(config, templates, lambdas):
    """Bake Dynamic Templates into HTML using Mustache Templates"""
    logger.info('Baking Dynamic Templates into HTML')
    for template in templates:
        try:
            logger.debug('Found Template: %s', template['name'])
            template['html'] = _htmlstache(config, template['body'], lambdas)
        except RuntimeError as e:
            logger.error("Error Baking Dynamic Templates: %s" % template, e)


@analyze
def serve(config, directory_path, version=None):
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
    _params = newdict(post, {'body': md.markdown(post['body'])})
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(_get_template_path(config, template_name), _params)


@analyze
def _htmlstache(config, template, lambdas=None):
    """Convert Markdown-YAML from its Mustache Template into HTML"""
    _params = {}
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
    renderer = pystache.Renderer(search_dirs=[config["recipe_root"] + os.sep + "templates"], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render(template, _params)


@analyze
def _textstache(config, content, template_name, lambdas=None):
    """Convert PlainText-YAML from its Mustache Template into HTML"""
    _params = newdict(content, {'body': content['body']})
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
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
    return parser.parse_args(args[1:])


### MAIN ###

def main():
    """Let's cook an Apple Pie:"""
    logger.info('Understanding config')
    args = _parse_cmd_args(sys.argv)
    sys_config = load_config("config.yml")
    config_path = args.config[0]
    user_config = load_config(config_path)
    # Merge configs if necessary
    config = sys_config if not user_config else dict(sys_config, **user_config)

    logger.info('Checking if Recipes are required')
    _download_recipe(config, args.recipe[0]) if args.recipe[0] != "recipe" else logger.info('Using default recipe')

    to_serve = True if "serve" in args.string_options else False

    logger.info('Cooking now')
    contents = load_contents(config)
    dynamic_templates = load_dynamic_templates(config)
    style, script, lambdas = load_recipes(config, contents, dynamic_templates)
    pie = bake(config, contents, dynamic_templates, style, script, lambdas,
               minify=to_serve)

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
