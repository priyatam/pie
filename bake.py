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

    
def main():
    """
    Let's cook an Apple Pie.
    """

    config = load_config()
    print config    


if __name__ == '__main__':
    main()
