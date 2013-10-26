#!/usr/bin/env python
"""
    Functions for misc utilities.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import logging
import logging.config
import os
import sys
import yaml
import time
import argparse
from datetime import datetime
from codecs import open
from functools import wraps
from subprocess import Popen, PIPE


logger = logging.getLogger('pielogger')


def get_logger():
    """Loads logging.yml and returns appropriate logger"""
    logging_conf = open('logging.yml', 'r')
    logging.config.dictConfig(yaml.load(logging_conf))
    logging_conf.close()
    return logging.getLogger('pielogger')


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


def load_config(config_path):
    """Loads configuration from config.yml"""
    with open(config_path, "r", "utf-8") as fin:
        user_config = yaml.load(fin.read())
    with open("config.yml", "r", "utf-8") as fin:
        sys_config = yaml.load(fin.read())
    config = dict(sys_config, **user_config)
    config["templates_path"] = config["recipe_root"] + os.sep + "templates"
    config["lambdas_path"] = config["recipe_root"] + os.sep + "lambdas"
    sys.path.append(config['lambdas_path'])
    config["styles_path"] = config["recipe_root"] + os.sep + "styles"
    if not os.path.exists(config["recipe_root"]):
        logger.error("recipe folder folder does not exist. Exiting now")
        exit(1)
    if not os.path.exists(config["content"]):
        logger.error("content folder folder does not exist. Exiting now")
        exit(1)
    for element in ["templates", "lambdas", "styles"]:
        if not os.path.exists(config[element + "_path"]):
            logger.error(element + " folder does not exist. Exiting now")
            exit(1)
    return config


def format_date(fname):
    """Formats to internal date format"""
    return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def read(fname, subdir):
    """Reads subdir/fname as raw content"""
    with open(subdir + os.sep + fname, "r", "utf-8") as fin:
        return fin.read()


def read_yaml(subdir, fname):
    """Splits subdir/fname into a tuple of YAML and raw content"""
    with open(subdir + os.sep + fname, "r", "utf-8") as fin:
        yaml_and_raw = fin.read().split('\n---\n')
        if len(yaml_and_raw) == 1:
            return {}, yaml_and_raw[0]
        else:
            return yaml.load(yaml_and_raw[0]), yaml_and_raw[1]


def parse_cmdline_args(args):
    """Parse command line args"""
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="*", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yml"])
    parser.add_argument("--recipe", nargs=1, default=["recipe"])
    return parser.parse_args(args[1:])


def build_index_html(pie, config_path):
    """Builds Index"""
    path = os.path.dirname(os.path.realpath(config_path))
    os.chdir(path)
    os.system('mkdir .build') if not os.path.isdir(".build") else None
    open('.build/index.html', 'w', "utf-8").write(pie)
    logger.info('Generated ' + path + '/.build/index.html')


def serve_github(config, directory_path):
    """Serve baked index.html into gh-pages"""
    # TODO: Refactor this from brute force to git api
    proc = Popen(['git', 'config', "--get", "remote.origin.url"], stdout=PIPE)
    url = proc.stdout.readline().rstrip("\n")
    os.chdir(directory_path)
    os.system("mkdir deploy")
    os.system("mv .build/index.html deploy/")
    os.system("rm -rf .build")
    os.system("git clone -b gh-pages " + url + " .build")
    os.system("cp deploy/index.html .build/")
    os.system("cd .build; git add index.html; git commit -m 'new deploy " + str(datetime.now()) + "'; git push --force origin gh-pages")


def newdict(*dicts):
    """Creates a new dictionary out of several dictionaries"""
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict
