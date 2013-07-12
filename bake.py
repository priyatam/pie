#!/usr/bin/env python

"""
# bake.py
python bake.py layout.mustache page.md

## Process
1. Prepare the Crust by reading Markdown document and YAML data
2. Choose a Pan by adding the Crust to a Mustache Template.
3. Add ingredients by choosing a stylesheet (TODO)
4. Pick a Recipe. A recipe is nothing but a Mustache lambda (TODO)
5. Bake. This generates the final index file with wrapped html, js, css includes etc.

"""

from __future__ import with_statement
import sys, contextlib
import yaml, markdown as md, pystache
import xml.etree.ElementTree as ET

def prepare_crust(filename):
    ''' '''
    with contextlib.closing(open(filename)) as filename_fin:
        text, data = __read(filename_fin)
        return choose_pan(markstache(text, data), data)

def __read(port):
    ''' Splits file into a tuple of YAML and Markdown '''
    parts = port.read().split('\n---\n')
    if len(parts) == 1:
        return (parts[0], {})
    else:
        return (parts[1], yaml.load(parts[0]))


def markstache(template, data):
    ''' Expands Mustache templates from local YAML data and renders Markdown as HTML  '''
    return md.Markdown().convert(pystache.render(template, data))


def choose_pan(body, context):
    ''' Export Crust to a Pan as {{ body }}.
        A Pan is a template in Markdown'''

    doc = ET.fromstring('<html>%s</html>' % body)

    top = list(doc)
    take(top, context, 'h1', 'title')

    context['body'] = ''.join(ET.tostring(e, 'utf-8') for e in top)

    return context


def take(elems, context, tag, name):
    if not elems or elems[0].tag != tag:
        raise RuntimeError('Expected %s' % tag)
    context[name] = elems.pop(0).text
    return context

def page(layout, article):
    ''' Combines the page with template '''

    with contextlib.closing(open(layout)) as layout_fin:
        text, data = __read(layout_fin)
        html = md.Markdown().convert(text)
        # FIXME: header and footer mustache are not being applied
        return pystache.render(html, prepare_crust(article))


def add_ingredients(style):
    ''' Adds stylesheet
        Final output should be
        bake.py layout.mustache page.md style.css
        '''

    print 'TODO' + page

def bake(page):
    ''' Wrap the final page in Html5, CSS, JSS '''
    print 'TODO' + page


## Main ##

def main(layout, article):
    print page(layout, article)

if __name__ == '__main__':
    main(*sys.argv[1:])
