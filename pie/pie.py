#!/usr/bin/env python
"""
    DSL for making a frozen pie, a.k.a, a static website.
    TODO: Refactor

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
        Apache License v2.0; see LICENSE for more details.
"""

import json
import jsmin
import cssmin
import contents
import templates
import styles
import lambdas
from glob import glob
from utils import *


def prepare(args):
    """Preparing config"""
    config = load_config(args.root, args.contents[0])

    if "deploy" in args.deploy:
        to_serve = True
    else:
        to_serve = False

    bake(config, deploy=to_serve)

    if to_serve:
        serve(config, args.deploy)


def load(config, contents_data, templates_data):
    """Create a tuple of dicts of compiled styles, scripts, and lambdas, along with their dictionary data"""
    styles_path = config["styles_path"]
    raw_styles = [read(os.path.basename(fn), styles_path) for fn in glob(styles_path + os.sep + "*.css") if not fn.endswith("master.css")]

    scss_fname = styles_path + os.sep + " style.scss"
    if os.path.isfile(scss_fname):
        style = styles.build(config)
        raw_styles.append(style)

    mastercss_fname = styles_path + os.sep + "master.css"
    if os.path.isfile(mastercss_fname):
        style = read("master.css", styles_path)
        raw_styles.insert(0, style)

    final_style = "".join(raw_styles)
    default_script = [read('controller.js', '.')]
    scripts = default_script
    if config.get('routes'):
        scripts.append(default_script)
        scripts.append('/* User-defined scripts*/\n')
        scripts = [read(route, config['root_path']) for route in config["routes"]]
    lambdas_data = lambdas.load(config, contents_data, templates_data)

    return final_style, scripts, lambdas_data


def bake(config, deploy=False):
    """Bakes contents, templates, scripts, and styles together"""
    params = {"title": config['title']}
    logger.info('Baking...')
    contents_data = contents.load(config)
    templates_data = templates.load(config)

    style, scripts, lambdas_data = load(config, contents_data, templates_data)

    logger.info('Baking contents and templates')
    contents.bake(config, contents_data, lambdas_data)
    templates.bake(config, templates_data, lambdas_data)

    params.update({"json_data": json.dumps(contents_data + templates_data)})

    logger.info('Baking styles and scripts')
    final_script = "".join(scripts)
    if deploy:
        params.update({"style_sheet": cssmin.cssmin(style), "script": jsmin.jsmin(final_script)})
    else:
        params.update({"style_sheet": style, "script": final_script})

    logger.info('Baking lambdas')
    params.update(lambdas_data)
    params.update({"config": config})

    logger.info('Compiling assets into an index page')
    pie = merge_pages(config, templates.get_index(config), params)
    build_index_html(pie, config)

    return pie


def serve(config, version=None):
    """Serves"""
    logger.info("Serving ... currently supports only gh-pages")
    directory_path = os.path.dirname(os.path.realpath(config.root))
    serve_github(config, directory_path)


if __name__ == '__main__':
    logger = get_logger()
    args = parse_cmdline_args(sys.argv)
    logger.info('Starting ...')
    prepare(args)
    logger.info('Finished')
