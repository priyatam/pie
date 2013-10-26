#!/usr/bin/env python
"""
    Functions for Templates.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import os
import markdown as md
import pystache
from utils import *


@analyze
def load_dynamic(config):
    """Create a dictionary for retrieving template's raw body, metadata, and compiled HTML"""
    templates = []
    path = config["templates_path"]
    for fname in os.listdir(path):
        if fname.endswith('.mustache'):
            try:
                meta, raw = read_yaml(path, fname)
                if meta.get('_type', 'simple') == 'dynamic':
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
def bake(config, templates, lambdas):
    """Bake Dynamic Templates into HTML using Mustache Templates"""
    logger.info('Baking Dynamic Templates into HTML')
    for template in templates:
        try:
            logger.debug('Found Template: %s', template['name'])
            template['html'] = to_htmlstache(config, template['body'], lambdas)
        except RuntimeError as e:
            logger.error("Error Baking Dynamic Templates: %s" % template, e)


@analyze
def to_markstache(config, post, template_name, lambdas=None):
    """Convert Markdown-YAML from its Mustache Template into HTML"""
    _params = newdict(post, {'body': md.markdown(post['body'])})
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
    renderer = pystache.Renderer(search_dirs=[config["templates_path"]], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(get_path(config, template_name), _params)


@analyze
def to_htmlstache(config, template, lambdas=None):
    """Convert Markdown-YAML from its Mustache Template into HTML"""
    _params = {}
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
    renderer = pystache.Renderer(search_dirs=[config["templates_path"]], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render(template, _params)


@analyze
def to_textstache(config, content, template_name, lambdas=None):
    """Convert PlainText-YAML from its Mustache Template into HTML"""
    _params = newdict(content, {'body': content['body']})
    _params.update(lambdas) if lambdas else logger.debug('No Lambdas provided')
    renderer = pystache.Renderer(search_dirs=[config["templates_path"]], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(get_path(config, template_name), _params)


@analyze
def get_path(config, name):
    """For given name, return the template path from config"""
    return config["templates_path"] + os.sep + name

