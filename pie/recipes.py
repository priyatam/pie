#!/usr/bin/env python
"""
    Functions for Recipes.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import os
from glob import glob
import json
import jsmin
import cssmin
import pystache

import contents
import templates
import styles
import lambdas
from utils import *


@analyze
def load(config, contents_data, dynamic_templates):
    """Create a tuple of dictionaries, each providing  access to compiled style, script, and raw lambdas,
    along with their dictionary data"""
    styles_path = config["styles_path"]
    raw_styles = [read(os.path.basename(fn), styles_path) for fn in glob(styles_path + os.sep + "*.css")
                  if not fn.endswith("master.css")]

    scss_fname = styles_path + os.sep + "style.scss"
    if os.path.isfile(scss_fname):
        style = styles.compile(config)
        raw_styles.append(style)

    mastercss_fname = styles_path + os.sep + "master.css"
    if os.path.isfile(mastercss_fname):
        style = read("master.css", styles_path)
        raw_styles.insert(0, style)

    final_style = "".join(raw_styles)

    script = read("script.js", config["lib"])

    lambdas_data = lambdas.load(config, contents_data, dynamic_templates)

    return final_style, script, lambdas_data



@analyze
def bake(config, contents_data, dynamic_templates, style, script, lambdas_data,
         minify=False):
    """Bake recipes with given style and script into a single index.html
        along with a json of style, script, and content"""
    params = {"title": config['title']}

    logger.info('Baking Contents and Dynamic Templates')
    contents.bake(config, contents_data, lambdas_data)

    templates.bake(config, dynamic_templates, lambdas_data)
    params.update({"json_data": json.dumps(contents_data + dynamic_templates)})

    logger.info('Baking Styles and Scripts')
    if minify:
        params.update({"style_sheet": cssmin.cssmin(style), "script": jsmin.jsmin(script)})
    else:
        params.update({"style_sheet": style, "script": script})

    logger.info('Baking Lambdas')
    params.update(lambdas_data)

    logger.info('Baking Config')
    params.update({"config": config})

    logger.info('Generating root index.html using index.mustache')
    _index_page = templates.get_path(config, "index.mustache")
    renderer = pystache.Renderer(search_dirs=[config["templates_path"]], file_encoding="utf-8", string_encoding="utf-8")

    return renderer.render_path(_index_page, params)


@analyze
def download(config, name):
    """Download recipes from github repo"""
    # TODO: Refactor this from brute force to git api
    os.system("rm -rf .build")
    os.system("rm -rf recipe.old")
    os.system("git clone " + config["recipes_repo"] + " .build")
    os.system("mv recipe recipe.old")
    os.system("cp -R .build/" + name + " recipe")

