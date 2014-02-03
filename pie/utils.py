#!/usr/bin/env python
"""
    Utility functions shared across modules.

    copyright:
        (c) 2014 by Priyatam Mudivarti
    license:
        Apache License v2.0; see LICENSE for more details.
"""

import logging
import logging.config
import yaml
import time
import argparse
import pystache
import os
import sys
import boto
import boto.s3
from boto.s3.key import Key
from codecs import open
from datetime import datetime
from glob import glob
from functools import wraps


def get_logger():
    """Loads logging.yml and returns appropriate logger"""
    logging_conf = open('logging.yml', 'r')
    logging.config.dictConfig(yaml.load(logging_conf))
    logging_conf.close()
    return logging.getLogger('pielogger')

logger = get_logger()

def analyze(func):
    """A debugger that dumps a docstring along with func args passed in"""
    argnames = func.func_code.co_varnames[:func.func_code.co_argcount]
    fname = func.func_name

    @wraps(func)
    def wrapper(*args, **kwds):
        logger.debug("<--->")
        for i in (a for a in zip(argnames, args) + kwds.items()):
            logger.debug("%s: %s", fname, func.__doc__)
            logger.debug(i)
        logger.debug("<--->")
        return func(*args, **kwds)

    return wrapper


def load_config(root_path, contents_path):
    """Loads configuration from user supplied config.yml"""
    if not os.path.exists(root_path):
        logger.error("'root' folder folder does not exist. Exiting now")
        exit(1)
    with open(root_path + os.sep + "config.yml", "r", "utf-8") as fin:
        config = yaml.load(fin.read())
    if not os.path.exists(contents_path):
        logger.error("contents folder folder does not exist. Exiting now")
        exit(1)

    config["root_path"] = root_path
    config["contents_path"] = contents_path
    config["templates_path"] = root_path + os.sep + "templates"
    config["lambdas_path"] = root_path + os.sep + "lambdas"
    config["styles_path"] = root_path + os.sep + "styles"
    config["master_css_fname"] = config["styles_path"] + os.sep + "master.css"
    config["scss_fname"] = config["styles_path"] + os.sep + "child.scss"
    config["index_html"] = config["root_path"] + os.sep + ".build" + os.sep + "index.html"

    sys.path.append(config['lambdas_path'])

    for element in ["templates", "lambdas"]:
        if not os.path.exists(config[element + "_path"]):
            logger.error(element + " folder does not exist. Exiting now")
            exit(1)

    return config


def format_date(fname):
    """Formats to internal date format"""
    return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def read(fname, directory=None):
    """Reads fname as raw content from dir"""
    if directory:
        path = directory + os.sep + fname
    else:
        path = fname
    with open(path, "r", "utf-8") as fin:
        return fin.read()


def read_yaml(directory, fname):
    """Splits subdir/fname into a tuple of YAML and raw content"""
    with open(directory + os.sep + fname, "r", "utf-8") as fin:
        yaml_and_raw = fin.read().split('\n---\n')
        if len(yaml_and_raw) == 1:
            return {}, yaml_and_raw[0]
        else:
            return yaml.load(yaml_and_raw[0]), yaml_and_raw[1]


def parse_cmdline_args(args):
    """Parse command line args"""
    parser = argparse.ArgumentParser(description='Frozen Pie: A minimalist static site generator and router.')
    parser.add_argument("root", type=str,
                        help='path to root project folder containing templates, styles, lambdas, and config.yml')
    parser.add_argument("contents", type=str,
                        help='path to contents folder containing markdown, plaintext')
    parser.add_argument('-m', '--minify', type=str, nargs='0', default=False, help='minify')
    parser.add_argument('-d', '--deploy', type=str, nargs='?', default='s3',
                        help='s3')
    return parser.parse_args(args[1:])


def merge_pages(config, index_page, params):
    """Merges all posts, pages into an index_page"""
    renderer = pystache.Renderer(search_dirs=[config["templates_path"]], file_encoding="utf-8", string_encoding="utf-8")
    return renderer.render_path(index_page, params)


def build_index_html(pie, config):
    """Builds Index"""
    os.chdir(config['root_path'])
    if not os.path.exists('site'):
        os.makedirs('site')
    open('site/index.html', 'w', "utf-8").write(pie)
    logger.info('Generated ' + config['root_path'] + '/site/index.html')


def serve_s3(config):
    """Serve baked index.html and js to S3. AWS_ACCESS_KEY_ID amd AWS_SECRET_ACCESS_KEY must be in environ """
    connection = boto.connect_s3(os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])
    bucket = connection.create_bucket(config['s3_bucket'], location=boto.s3.connection.Location.DEFAULT)

    logger.info('Uploading %s to Amazon S3 bucket %s' % (config['index_html'], config['s3_bucket']))
    k = Key(bucket)
    k.key = 'index.html'
    k.set_contents_from_filename(config['index_html'])

    logger.info("Copying user js to S3")
    for jsfile in glob("js" + os.sep + "*.js"):
        k = Key(bucket)
        filename = "js/" + os.path.basename(jsfile)
        k.key = filename
        k.set_contents_from_filename(jsfile)


def newdict(*dicts):
    """Creates a new dictionary out of several dictionaries"""
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict
