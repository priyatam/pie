#!/usr/bin/env python
"""
Usage: python bake.py > index.html
Algo: Read config.yaml. For each post.md, process YAML, and apply its Mustache-HAML Template, and generate final HTML. Combine everything into index.html with minified CSS, JS.
"""
import os
import sys
import re
import time
from datetime import datetime
import json
import yaml
import markdown as md
import pystache
from hamlpy import hamlpy
import contextlib
import subprocess
from subprocess import Popen, PIPE, STDOUT


# Set config file path
if len(sys.argv) > 1:
    config_file_path = sys.argv[1]
else:
    config_file_path = "config.yaml"


def load_config():
    """Loads configuration from config.yaml"""
    with open(config_file_path, "r") as fin:
        return yaml.load(fin.read())


def load_assets(config):
    """Loads assets as raw content into a dictionary, looked up by its fname"""
    return lambda asset_type: {fname: _read(fname, asset_type) for fname in config[asset_type]}


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        if re.match(r'[A-Za-z\.0-9-_~]+', fname):
            yaml_data, md_content = _read_posts('posts', fname)
            fname = 'posts' + os.sep + fname
            post = {
                "name": fname,
                "body": md_content,  # raw, unprocessed markdown content
                "created_date": _format_date(fname, 'c'),
                "modified_date": _format_date(fname, 'm')
            }
            post.update(yaml_data)  # Merge Yaml data for future lookup
            posts.append(post)
        else:
            print """Filename format: ['a/A', 2.5, '_', '.', '-', '~']"""
            exit(1)

    return posts


def load_content(config):
    """Pre-process and load each asset type into a dict and return a tuple of such dicts"""

    # Html pre-procesors: HAML
    templates = load_assets(config)('templates')
    # TODO: hamlstache(config)

    # CSS pre-processors: SASS, LESS
    # TODO: __sassify(config), __lessen(config)
    styles = load_assets(config)('styles')
    __sassify(styles)

    # Js pre-processors: Coffeescript
    # TODO: make_coffeescript, make_clojurescript
    scripts = load_assets(config)('scripts')

    posts = load_posts(config)

    return templates, styles, scripts, posts


def bake(config, templates, posts, styles, scripts):
    """Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS
       NOTE: This function modifies 'posts' dictionary by adding a new posts['html'] element"""
    for post in posts:
        converted_html = _markstache(post, templates[post['template']])  # each post can have its own template
        post['html'] = converted_html

    style_sheets = [styles[key] for key in config['styles']]
    style_sheet = "".join(style_sheets)
    scripts = [scripts[key] for key in config['scripts']]
    script = "".join(scripts)
    content = pystache.render(templates['index.html.mustache'],
                              {"style_sheet": style_sheet,
                               "script": script,
                               "json_data": json.dumps(posts), "relative_path": config['relative_path'],
                               "title": config['title']
                               })
    return content


def _read(fname, subdir):
    """Reads subdir/<fname> as raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        return fin.read()


def _read_posts(subdir, fname):
    """Splits file into a tuple of YAML and Markdown content"""
    with open(subdir + os.sep + fname, "r") as fin:
        yaml_and_md = fin.read().split('\n---\n')
        if len(yaml_and_md) == 1:
            return {}, yaml_and_md[0]
        else:
            return yaml.load(yaml_and_md[0]), yaml_and_md[1]


def _markstache(post, template):
    """Converts Markdown/Mustache/YAML to HTML."""
    html_md = md.markdown(post['body'].decode("utf-8"))
    _params = {}
    _params.update(post) # Post Dict with YAML and other meta data
    _params.update({'body': html_md})
    return pystache.render(template, _params)


def __sassify(styles):
    """Compiles SASS assets. FIXME: Do not modify config"""
    for key in styles.keys():
        match = re.search(r'(.+?)\.sass$', key)
        if match:
            if (_check_cmd("sass")):
                p = Popen(['sass', '-s'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
                stdout_data = p.communicate(input=styles[key])[0]
                styles[key] = stdout_data  # FIXME: mutation
            else:
                print "sass command not found. Install using rubygems"
                exit(1)


def _check_cmd(cmd):
    """Checks if 'cmd' is available on command line"""
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def _format_date(fname, datetype):
    """Returns a formatted fname.date"""
    if datetype == 'c':
        return datetime.strptime(time.ctime(os.path.getctime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")
    if datetype == 'm':
        return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def main():
    """Let's cook an Apple Pie"""
    config = load_config()
    templates, styles, scripts, posts = load_content(config)
    output = bake(config, templates, posts, styles, scripts, )
    print output


if __name__ == '__main__':
    main()
