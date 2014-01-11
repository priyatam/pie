#!/usr/bin/env python
"""
    DSL for making a static site with dynamic powers.

    usage:
        pie.py --help

    algo:
        Read config.yml.
        For each post.md and page.md, process YAML and apply Mustache templates.
        If template#_type=dynamic generate templates,
        Combine all posts and pagse, generate final HTML with a minified CSS, JS.

    copyright:
        (c) 2014 by Priyatam Mudivarti

    license:
        Apache License v2.0; see LICENSE for more details.
"""

import json
import jsmin
import cssmin
import contents
import templates
import lambdas
from utils import *


def prepare(args):
    """Preparing config"""
    config = load_config(args.root, args.contents)

    if "deploy" in args.deploy:
        to_deploy = True
    else:
        to_deploy = False

    bake(config, deploy=to_deploy)

    if to_deploy:
        serve(config, args.deploy)


def mix(config, contents_data, templates_data):
    """Create a tuple of dicts of compiled styles, scripts, and lambdas, along with their dictionary data"""
    raw_styles = [read(os.path.basename(fn), config["styles_path"])
                  for fn in glob(config["styles_path"] + os.sep + "*.css") if not fn.endswith("master.css")]

    if os.path.isfile(config['scss_fname']):
        style = read("child.css", styles_path)
        raw_styles.append(style)
    if os.path.isfile(config['master_css_fname']):
        style = read(config['master_css_fname'])
        raw_styles.insert(0, style)
    final_style = "".join(raw_styles)

    default_script = [read('controller.js', os.path.dirname(__file__))]
    scripts = default_script
    if config.get('routes'):
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

    style, scripts, lambdas_data = mix(config, contents_data, templates_data)

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
    """Serves to S3 or Dropbox"""
    logger.info("Serving ... currently supports only S3")
    directory_path = os.path.dirname(os.path.realpath(config.root))
    serve_s3(config, directory_path)


if __name__ == '__main__':
    logger = get_logger()
    args = parse_cmdline_args(sys.argv)
    logger.info('Starting ...')
    prepare(args)
    logger.info('Finished')
