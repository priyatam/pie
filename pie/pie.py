#!/usr/bin/env python
"""
    DSL for making a frozen pie, a.k.a, a static website.

    run:
        pie.py
          or
        pie.py --config=path_to_config_yml
    host:
        pie.py serve (pushes to your github pages)
    algo:
        Read config.yml.
        For each post.md, process YAML, and apply its Mustache Templates, and generate final HTML.
        Combine everything into a single index.html with a minified CSS, JS.
        See docs for more info.
    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import contents
import templates
import recipes
from utils import *


def prepare():
    """Let's cook an Apple Pie:"""
    config = load_config(config_path)

    if "serve" in args.string_options:
        to_serve = True
    else:
        to_serve = False

    bake(config, to_serve=to_serve)

    if to_serve:
        serve(config, config_path)


def add_recipes(config, cmds):
    """Add recipes, if any"""
    logger.info('Checking if Recipes are required')
    recipes.download(config, cmds.recipe[0]) if cmds.recipe[0] != "recipe" else logger.info('Using default recipe')


def bake(config, to_serve=False):
    """Bakes Contents, Templates, and Recipes together"""
    logger.info('Baking...')
    contents_data = contents.load(config)
    dynamic_templates = templates.load_dynamic(config)
    style, script, lambdas_data = recipes.load(config, contents_data, dynamic_templates)
    pie = recipes.bake(config, contents_data, dynamic_templates, style, script, lambdas_data, minify=to_serve)

    build_index_html(pie, config_path)

    return pie


def serve(config, version=None):
    """Serves"""
    logger.info("Serving ... currently supports only gh-pages")
    directory_path = os.path.dirname(os.path.realpath(config_path))
    serve_github(config, directory_path)


if __name__ == '__main__':
    logger = get_logger()

    logger.info('Setting global config path')
    args = parse_cmdline_args(sys.argv)
    config_path = args.config[0]

    logger.info('Starting ...')
    prepare()
    logger.info('Finished')
