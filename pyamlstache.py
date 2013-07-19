#!/usr/bin/env python
"""
Render a Haml Template with Mustache and Yaml in Python.

Usage:
    pyamlstache.py index.haml.mustache > index.html

"""

import sys
import contextlib
import yaml
import pystache
from hamlpy import hamlpy


def process(filename):
    ''' Core processing '''

    with contextlib.closing(open(filename)) as fin:
        haml, data = __read(fin)
        haml_stached = pystache.render(haml, data)
        hamlParser = hamlpy.Compiler()
        html = hamlParser.process(haml_stached)
        return html


def __read(fin):
    ''' Loads file into a tuple of YAML and HAML '''

    parts = fin.read().split('\n---\n')
    if len(parts) == 1:
        return parts[0], {}
    else:
        return parts[1], yaml.load(parts[0])


## Main ##
def main(haml):
    print 'Converting a Haml Template with Mustache and Yaml ...'
    print process(haml)

if __name__ == '__main__':
    main(sys.argv[1])
