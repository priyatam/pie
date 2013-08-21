import logging, logging.config
import os
import yaml
import time
from datetime import datetime
from codecs import open
from functools import wraps


logger = logging.getLogger('pielogger')

def get_logger():
    """Loads logging.yml and returns appropriate logger"""
    loggingConf = open('logging.yml', 'r')
    logging.config.dictConfig(yaml.load(loggingConf))
    loggingConf.close()
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
    config["styles_path"] = config["recipe_root"] + os.sep + "styles"
    return config


def format_date(fname):
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


def newdict(*dicts):
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict
