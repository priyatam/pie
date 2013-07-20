#!/usr/bin/env python
"""
Usage:
python bake.py > index.html

Algo:
Read config.yaml
For each post, generate complete html by applying templates
Generate index.html with included CSS

"""

import os, time
import yaml, markdown as md, pystache
import json

def load_config():
    """Loads configuration from config.yaml""" 
    with open("config.yaml", "r") as fin:
        params = fin.read()
        #templates = [ p for p in params .find('template') for  for p in params if p.find('template') is not -1 ]
        
        return yaml.load(params)

def load_content(config):
    """Reads templates, scripts, styles and stores their raw content in dictionaries"""  
    content = {}         

    # Group by type in config
    templates = dict(config, 'templates')
    styles = dict(config, 'styles')
    scripts = dict(config, 'scripts')
    
    # Merge dictionaries
    content.update(templates)
    content.update(styles)
    content.update(scripts)

    return content


def dict(config, key):
    """Creates a dictionary of key->config[key] raw content"""
    return {x: read(key, x) for x in config[key]}
    

def read(subdir, filename):
        """Reads subdir/<filename> as raw content"""                              
        with open(subdir + os.sep + filename, "r") as fin: 
            return fin.read()    


def read_markdown(subdir, filename):
    """Splits Markdown file into a tuple of YAML and content"""
    with open(subdir + os.sep + filename, "r") as fin:                
        yaml_and_md = fin.read().split('\n---\n')
        if len(yaml_and_md) == 1:
            return {}, yaml_and_md[0]
        else:
            return yaml.load(yaml_and_md[0]), yaml_and_md[1]


def main():
    """
    Let's cook an Apple Pie.
    """

    config = load_config()
    print type(config)
    print config    
    
    content = load_content(config)
    print type(content)
    for i in content.keys():
        print i


if __name__ == '__main__':
    main()
