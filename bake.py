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
from scss import Scss


def load_config(config_path):
    """Loads configuration from config.yaml"""
    with open(config_path, "r") as fin:
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
    # Compile HAML Templates
    compile_assets(config, 'templates')(compile_haml, 'haml','html')        
    time.sleep(1) # else, next guy won't see the new file
    templates = load_assets(config)('templates', 'html')

    # Compile SASS
    sass_css = _scssify(config)
    # sass_css = compile_assets(config, 'styles')(compile_sass, 'sass','css')      
    css_styles = load_assets(config)('styles', 'css')   
    styles = __newdict(css_styles, sass_css)    
    
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
    _params = __newdict(post, {'body': html_md})
    return pystache.render(template, _params)


def compile_assets(config, asset_type):
    def _compile(__compile, _from, _to,):
        for fname in os.listdir(asset_type):
            if fname.endswith(_from):
                raw_data = __compile(asset_type, fname) # Inner Closure (__compile) applying on outer closure (_compile)
                open(asset_type + os.sep + fname.replace(_from, _to), 'w').write(raw_data)
                return raw_data
    return _compile


def compile_haml(asset_type, fname):
    data, haml = _read_yaml(asset_type, fname)
    return hamlpy.Compiler().process(haml)
    
# FIXME: See compile_assets, compile_haml    
def compile_sass(asset_type, fname):
    return Scss().compile(_read(fname, asset_type)) 

# TODO: Remove after compile_sass is working
def _scssify(config):
    """Compiles SCSS assets."""
    styles = {}
    for sname in os.listdir("styles"):
        match = re.search(r'(.+?)\.sass$', sname)
        if match:
            scss_compiler = Scss() #
            style = _read(sname, "styles") #
            styles[sname] = scss_compiler.compile(style) # add css             
            open('styles' + os.sep + sname.replace('sass', 'css'), 'w').write(style) 
            return styles


def _format_date(fname, datetype):
    """Returns a formatted fname.date"""
    if datetype == 'c':
        return datetime.strptime(time.ctime(os.path.getctime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")
    if datetype == 'm':
        return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")

def __newdict(*dicts):
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict

def main(config_path):
    """Let's cook an Apple Pie"""
    config = load_config(config_path)
    templates, styles, scripts, posts = load_content(config)
    output = bake(config, templates, posts, styles, scripts, )
    print output


if __name__ == '__main__':
    config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"             
    main(config_path)