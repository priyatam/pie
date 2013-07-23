#!/usr/bin/env python
"""
Usage:
python bake.py > index.html

Algo:
Read config.yaml
For each post, generate complete html by applying Mustache templates
Generate index.html with included CSS, JS

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
import json
from datetime import datetime
import subprocess

if len(sys.argv) > 1:
    config_file_path = sys.argv[1]
else:
    config_file_path = "config.yaml"


def cmd_exists(cmd):
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def load_config():
    """Loads configuration from config.yaml"""
    with open(config_file_path, "r") as fin:
        return yaml.load(fin.read())


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        if re.match(r'[A-Za-z\.0-9-_~]+', fname):
            yaml_data, md_data = read_markdown('posts', fname)
            fname = 'posts' + os.sep + fname
            post = {
                "name": fname,
                "body": md_data,  # raw, unprocessed md
                "created_date": _format_date(fname, 'c'),
                "modified_date": _format_date(fname, 'm')
            }
            post.update(yaml_data)  # Merge Yaml data
            posts.append(post)
        else:
            print """File name format: uppercase/lowercase letters, decimal digits, hyphen, period, underscore, and tilde only."""                     
            exit(1)

    return posts


def load_metacontent(config):
    """Reads templates, scripts, styles and stores them as dictionaries"""
    metacontent = {}
    # Group these by type in config
    templates = rawcontent_by_fname(config, 'templates')
    config = ppsass_by_fname(config, 'styles')
    styles = rawcontent_by_fname(config, 'styles')
    scripts = rawcontent_by_fname(config, 'scripts')
    # Merge them
    metacontent.update(templates)
    metacontent.update(styles)
    metacontent.update(scripts)

    return metacontent


def ppsass_by_fname(config, subdir):
    for sass_or_css_file in os.listdir(subdir):
        match = re.search(r'(.+?)\.sass$', sass_or_css_file)
        if match:
            if (cmd_exists("sass")):
                out_file = match.group(1) + ".css"
                cmd = "sass " + subdir + "/" + sass_or_css_file + " > " + subdir + "/" + out_file
                os.system(cmd)
                config[subdir].remove(sass_or_css_file)
                config[subdir].append(out_file)
            else:
                print "sass command not found\ninstall using rubygems"
                exit(1)
    return config


def rawcontent_by_fname(config, key):
    """Creates a dictionary of fname->raw_content, where raw_content is config(key)"""
    return {fname: _read(key, fname) for fname in config[key]}


def read_markdown(subdir, fname):
    """Splits Markdown file into a tuple of YAML and content"""
    with open(subdir + os.sep + fname, "r") as fin:
        yaml_and_md = fin.read().split('\n---\n')
        if len(yaml_and_md) == 1:
            return {}, yaml_and_md[0]
        else:
            return yaml.load(yaml_and_md[0]), yaml_and_md[1]


def markstache(post, template):
    """Expands Mustache templates from local YAML data and renders Markdown as HTML"""
    raw_md = md.markdown(post['body'].decode("utf-8"))
    return pystache.render(template, {"body": raw_md})


def bake(config, metacontent, posts):
    """ Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS """
    # Stache
    for post in posts:
        post['html'] = markstache(post, metacontent[post['template']])  # every post can have its template

    style_sheets = [metacontent[key] for key in config['styles']]
    style_sheet = "".join(style_sheets)

    scripts = [metacontent[key] for key in config['scripts']]
    script = "".join(scripts)

    content = pystache.render(metacontent['index.mustache'],
                              {"style_sheet": style_sheet, "script": script,
                               "json_data": json.dumps(posts), "relative_path": config['relative_path'],
                               "title": config['title']})
    print content


def _format_date(fname, type):
    """Returns a formatted fname.date"""
    if type == 'c':
        return datetime.strptime(time.ctime(os.path.getctime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")
    if type == 'm':
        return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y") 
    

def _read(subdir, fname):
    """Reads subdir/<fname> as raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        return fin.read()

def main():
    """Let's cook an Apple Pie"""
    config = load_config()
    metacontent = load_metacontent(config)
    posts = load_posts(config)
    bake(config, metacontent, posts)


if __name__ == '__main__':
    main()
