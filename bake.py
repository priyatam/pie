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


def load_config():
    """Loads configuration from config.yaml"""
    with open(config_file_path, "r") as fin:
        return yaml.load(fin.read())


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        if re.match(r'[A-Za-z\.0-9-_~]+', fname):
            yaml_data, md_data = _read_markdown('posts', fname)
            fname = 'posts' + os.sep + fname
            post = {
                "name": fname,
                "body": md_data,  # raw, unprocessed md
                "created_date": __format_date(fname, 'c'),
                "modified_date": __format_date(fname, 'm')
            }
            post.update(yaml_data)  # Merge Yaml data
            posts.append(post)
        else:
            print """File name format: uppercase/lowercase letters, decimal digits, hyphen, period, underscore, and tilde only."""
            exit(1)
            
    return posts

def run_asset_pipieline(config):
    """Run preprocessor asset pipeline """
    ## SASS
    config = __sassify(config, 'styles')
    ## TODO - Use Webassets - http://webassets.readthedocs.org/en/latest/generic/index.html


def load_metacontent(config):
    """Reads templates, scripts, styles and stores them as dictionaries"""
    metacontent = {}
    
    # Load templates, styles and scripts into a dict as fname: raw content
    templates = __rawcontent_by_fname(config, 'templates')
    styles = __rawcontent_by_fname(config, 'styles')
    scripts = __rawcontent_by_fname(config, 'scripts')
    metacontent.update(templates)
    metacontent.update(styles)
    metacontent.update(scripts)

    return metacontent


def bake(config, metacontent, posts):
    """ Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS """
    for post in posts:
        post['html'] = _markstache(post, metacontent[post['template']])  # every post can have its template

    style_sheets = [metacontent[key] for key in config['styles']]
    style_sheet = "".join(style_sheets)

    scripts = [metacontent[key] for key in config['scripts']]
    script = "".join(scripts)

    content = pystache.render(metacontent['index.mustache'],
                              {"style_sheet": style_sheet, "script": script,
                               "json_data": json.dumps(posts), "relative_path": config['relative_path'],
                               "title": config['title']})
    return content


def _read(subdir, fname):
    """Reads subdir/<fname> as raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        return fin.read()


def _read_markdown(subdir, fname):
    """Splits Markdown file into a tuple of YAML and content"""
    with open(subdir + os.sep + fname, "r") as fin:
        yaml_and_md = fin.read().split('\n---\n')
        if len(yaml_and_md) == 1:
            return {}, yaml_and_md[0]
        else:
            return yaml.load(yaml_and_md[0]), yaml_and_md[1]


def _markstache(post, template):
    """Expands Mustache templates from local YAML data and renders HTML"""
    html_md = md.markdown(post['body'].decode("utf-8"))
    _params = {}
    _params.update(post)
    _params.update({'body': html_md })
    return pystache.render(template, _params)
  

def _invoke_cmd(cmd):
    """Runs 'cmd' on command line"""
    return subprocess.call("type " + cmd, shell=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def __sassify(config, subdir):
    """Compiles SASS assets. FIXME: Do not modify the code"""
    for sass_or_css_file in os.listdir(subdir):
        match = re.search(r'(.+?)\.sass$', sass_or_css_file)
        if match:
            if (_invoke_cmd("sass")):
                out_file = match.group(1) + ".css"
                cmd = "sass " + subdir + "/" + sass_or_css_file + " > " + subdir + "/" + out_file
                os.system(cmd)
                # config[subdir].remove(sass_or_css_file)
                config[subdir].append(out_file)
            else:
                print "sass command not found. Install using rubygems"
                exit(1)
    return config


def __rawcontent_by_fname(config, key):
    """Creates a dictionary of fname->raw_content, where raw_content is config(key)"""
    return {fname: _read(key, fname) for fname in config[key]}


def __format_date(fname, datetype):
    """Returns a formatted fname.date"""
    if datetype == 'c':
        return datetime.strptime(time.ctime(os.path.getctime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")
    if datetype == 'm':
        return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y") 


def main():
    """Let's cook an Apple Pie"""
    config = load_config()
    run_asset_pipieline(config)
    metacontent = load_metacontent(config)
    posts = load_posts(config)
    output = bake(config, metacontent, posts)
    
    print output
    

if __name__ == '__main__':
    main()
