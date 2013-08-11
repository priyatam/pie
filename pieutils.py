import yaml
import time
from datetime import datetime
import os
from codecs import open


def load_config(config_path):
    """Loads configuration from config.yaml"""
    with open(config_path, "r", "utf-8") as fin:
        return yaml.load(fin.read())


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
