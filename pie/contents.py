#!/usr/bin/env python
"""
    Functions for Contents written in Markdown, PlainText.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import sys
import os
import templates
from utils import *


@analyze
def load(config):
    """Create a dictionary for retrieving content's raw body, metadata, and future compiled html"""
    contents = []
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
                contents.append(content)
            except RuntimeError:
                logger.error("Error while reading content: %s:\n%s" % (fname, sys.exc_info()[0]))
        else:
            logger.warning("Incorrect Extension: %s" % fname)
    return contents


@analyze
def bake(config, contents, lambdas):
    """Baking Contents into HTML using Mustache Templates"""
    logger.info('Baking Contents into HTML')
    for content in contents:
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
            logger.error("Error Baking Contents: %s" % content, e)

