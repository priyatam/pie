#!/usr/bin/env python
"""
    Functions for creating, accessing contents written in Markdown, PlainText.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache License v2.0; see LICENSE for more details.
"""

import sys
import os
import templates
from utils import *


@analyze
def load(config):
    """Create a dictionary for retrieving content's raw body, metadata, and future compiled html"""
    data = []
    path = config['content']
    for fname in os.listdir(path):
        if fname.endswith('.md') or fname.endswith('.txt'):
            try:
                meta, raw = read_yaml(path, fname)
                content = {
                    "name": meta.get("_type", "content") + "/" + fname,
                    "body": raw,
                    "modified_date": format_date(path + os.sep + fname)
                }
                content.update(meta)
                data.append(content)
            except:
                logger.error("Error while reading content: %s: %s" % (fname, sys.exc_info()[0]))
        else:
            logger.warning("Incorrect Extension: %s" % fname)
    return data


@analyze
def bake(config, contents_data, lambdas):
    """Baking contents_data into HTML using Mustache Templates"""
    logger.info('Baking contents_data into HTML')
    for content in contents_data:
        try:
            if content['name'].endswith('.txt'):
                template = content.get('template', config['default_template'])
                logger.debug('Found Template: %s for content: %s', template, content['name'])
                content['html'] = templates.to_textstache(config, content, template, lambdas)
                del content['body']
            elif content['name'].endswith('.md'):
                template = content.get('template', config['default_template'])
                logger.debug('Found Template: %s for content: %s', template, content['name'])
                content['html'] = templates.to_markstache(config, content, template, lambdas)
        except RuntimeError as e:
            logger.error("Error Baking contents_data: %s" % content, e)

