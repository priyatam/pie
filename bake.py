#!/usr/bin/env python
"""
Usage:
python bake.py > index.html

Algo:
Read config.yaml
For each post, generate complete html by applying templates
Generate index.html with included CSS

"""

from __future__ import with_statement
import os, time
import yaml, markdown as md, pystache
import json

posts = []
config = None

class Config(object):
    def __init__(self, yaml_data):
        self.yaml_data = yaml_data

    def post_template(self):
        template_file = self.yaml_data.get("post_template")
        filename = "templates/" + template_file
        with open(filename, "r") as filename_fin:
            return filename_fin.read()

    def index_template(self):
        template_file = self.yaml_data.get("index_template")
        filename = "templates/" + template_file
        with open(filename, "r") as filename_fin:
            return filename_fin.read()


    def style_sheet(self):
        css_file = self.yaml_data.get("theme")
        filename = "static/" + css_file
        with open(filename, "r") as filename_fin:
            return filename_fin.read()


    def script(self):
        script_file = self.yaml_data.get("script")
        filename = "static/" + script_file
        with open(filename, "r") as filename_fin:
            return filename_fin.read()


def Post(front_matter, raw_content, name, ctime, mtime):
        data = {
            "body" : raw_content,
            "name" : name,
            "ctime" : ctime,
            "mtime" : mtime
            }
        data.update(front_matter)
        return data


def read_config():
    with open("config.yaml", "r") as content_file:
        text = content_file.read()
        return yaml.load(text)


def prepare_crust():
    ''' '''
    global config
    global posts
    config_data = read_config()
    config = Config(config_data)

    for filename in os.listdir("posts"):
        filename = "posts/" + filename
        with open(filename, "r") as filename_fin:
            text, data = __read(filename_fin)
            ctime = time.ctime(os.path.getmtime(filename))
            mtime = time.ctime(os.path.getctime(filename))
            post = Post(data, text, filename, ctime, mtime)
            shake_pan(post)
            posts.append(post)


def __read(port):
    ''' Splits file into a tuple of YAML and Markdown '''
    parts = port.read().split('\n---\n')
    if len(parts) == 1:
        return (parts[0], {})
    else:
        return (parts[1], yaml.load(parts[0]))


def markstache(post):
    ''' Expands Mustache templates from local YAML data and renders Markdown as HTML  '''
    post["html"] = md.Markdown().convert(pystache.render(config.post_template(), post))
    return post


def shake_pan(post):
    ''' Export Crust to a Pan as {{ body }}.
        A Pan is a template in Markdown'''
    return markstache(post)


def bake(style_sheet, script):
    ''' Wrap the final page in Html5, CSS, JS, POSTS '''
    print pystache.render(config.index_template(), { "style_sheet" : style_sheet, "script" : script, "json_data" : json.dumps(posts) })
## Main ##

def main():
    prepare_crust()
    # get ingredients
    style_sheet = config.style_sheet()
    script = config.script()
    bake(style_sheet, script)

if __name__ == '__main__':
    main()
