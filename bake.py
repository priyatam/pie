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
import subprocess
from scss import Scss


def load_config(config_filepath):
    """Loads configuration from config.yaml"""
    with open(config_filepath, "r") as fin:
        return yaml.load(fin.read())


def load_assets(config):
    """Loads assets as raw content into a dictionary, looked up by its fname.
    Closure accepts an asset_type ('templates', 'styles', 'posts', 'scripts') and a filter that filters based on file ext"""
    return lambda asset_type, filter: {fname: _read(fname, asset_type) for fname in os.listdir(asset_type) if fname.endswith(filter)}


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        if re.match(r'[A-Za-z\.0-9-_~]+', fname):
            yaml_data, md_content = _read_yaml('posts', fname)
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
    _hamlify(config)
    time.sleep(1) # else, next guy won't see the new file
    templates = load_assets(config)('templates', 'html')

    # CSS pre-processors: SASS, LESS
    compiled_styles = _scssify(config)
    css_styles = load_assets(config)('styles', 'css')   
    styles = {}    
    styles.update(css_styles)
    styles.update(compiled_styles)
    
    # Js pre-processors: Coffeescript
    # TODO: _make_coffeescript(config)
    scripts = load_assets(config)('scripts', 'js')

    posts = load_posts(config)

    return templates, styles, scripts, posts


def bake(config, templates, posts, styles, scripts):
    """Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS
       NOTE: This function modifies 'posts' dictionary by adding a new posts['html'] element"""
    for post in posts:
        converted_html = _markstache(post, templates[post['template']])  # each post can have its own template
        post['html'] = converted_html

    style_sheets = [styles[key] for key in os.listdir("styles")]
    style_sheet = "".join(style_sheets)
    scripts = [scripts[key] for key in os.listdir("scripts")]
    script = "".join(scripts)
    content = pystache.render(templates['index.mustache.html'],
                              {"style_sheet": style_sheet,
                               "script": script,
                               "json_data": json.dumps(posts), "relative_path": config['relative_path'],
                               "title": config['title']
                               })
    return content


def _read(fname, subdir):
    """Reads subdir/fname as raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        return fin.read()


def _read_yaml(subdir, fname):
    """Splits subdir/fname into a tuple of YAML and raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        yaml_and_raw = fin.read().split('\n---\n')
        if len(yaml_and_raw) == 1:
            return {}, yaml_and_raw[0]
        else:
            return yaml.load(yaml_and_raw[0]), yaml_and_raw[1]
        

def _markstache(post, template):
    """Converts Markdown/Mustache/YAML to HTML."""
    html_md = md.markdown(post['body'].decode("utf-8"))
    _params = {}
    _params.update(post) # Post Dict with YAML and other meta data
    _params.update({'body': html_md})
    return pystache.render(template, _params)


def _hamlify(config):
    """Compiles HAML with YAML into data, HTML"""
    for fname in os.listdir("templates"):
        match = re.search(r'(.+?)\.haml', fname)
        if match:
            data, haml = _read_yaml('templates', fname)
            fin_html = hamlpy.Compiler().process(haml)
            fout = open('templates' + os.sep + fname.replace('haml', 'html'), 'w')
            fout.write(fin_html)
            return data, haml
        

def _scssify(config):
    """Compiles SCSS assets."""
    styles = {}
    for sname in os.listdir("styles"):
        match = re.search(r'(.+?)\.sass$', sname)
        if match:
            scss_compiler = Scss()
            style = _read(sname, "styles")
            styles[sname] = scss_compiler.compile(style) # add css
            open('styles' + os.sep + sname.replace('sass', 'css'), 'w').write(style) 
            return styles


def _check_cmd(cmd):
    """Checks if 'cmd' is available on command line"""
    return subprocess.call("type " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0


def _format_date(fname, datetype):
    """Returns a formatted fname.date"""
    if datetype == 'c':
        return datetime.strptime(time.ctime(os.path.getctime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")
    if datetype == 'm':
        return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def main(config_filepath):
    """Let's cook an Apple Pie"""
    config = load_config(config_filepath)
    templates, styles, scripts, posts = load_content(config)
    output = bake(config, templates, posts, styles, scripts, )
    print output


if __name__ == '__main__':
    config_filepath = "config.yaml"
    if len(sys.argv) > 1:
        config_filepath = sys.argv[1]        
    main(config_filepath)
