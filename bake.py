#!/usr/bin/env python
"""
Usage: bake.py
Algo: Read config.yaml. For each post.md, process YAML, and apply its Mustache-HAML Template, and generate final HTML. 
Lastly, combine everything into a single index.html with a minified CSS, JS.
"""

import sys
import time
from datetime import datetime
from importlib import import_module
import json
import os
import re
import yaml
import markdown as md
import pystache
from hamlpy import hamlpy
from scss import Scss
import coffeescript

import cssmin
import jsmin
import argparse
from subprocess import Popen, PIPE


def load_config(config_path):
    """Loads configuration from config.yaml"""
    with open(config_path, "r") as fin:
        return yaml.load(fin.read())


def load_assets(config):
    """Loads assets as raw content into a dictionary, looked up by its fname.
    Closure accepts an asset ('templates', 'styles', 'posts', 'scripts') and a filter that filters based on file ext"""
    return lambda asset, filter: {fname: _read(fname, asset) for fname in os.listdir(asset) if fname.endswith(filter)}


def load_recipes(config):
    """Loads all pure functions from each module under recipes/ as a dictionary lookup by funcion name"""
    modules = [import_module("recipes." + recipe) for recipe in _recipes()]
    # To avoud namespace collisions, filename is a prefix to all functions defined in it
    # So default_hello_world
    functions_dict = {mod.__name__.strip("recipes.") + "_" + funcname: getattr(mod, funcname) for mod in modules for funcname in dir(mod) if not funcname.startswith("__")}
    return functions_dict


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        if re.match(r'[A-Za-z\.0-9-_~]+', fname):
            yaml_data, md_content = _read_yaml('posts', fname)
            fname = 'posts' + os.sep + fname
            post = {
                "name": fname,
                "body": md_content, # raw, unprocessed markdown content
                "modified_date": _format_date(fname)
            }
            post.update(yaml_data)  # Merge Yaml data for future lookup
            posts.append(post)
        else:
            print """Filename format: ['a/A', 2.5, '_', '.', '-', '~']"""
            exit(1)

    return posts


def compile_assets(config, asset_type):
    """Closure: Compiles asset types: css, js, html using pre-processors.
       Currently supports haml, scss, coffeescript."""

    def _compile(__compile, _from, _to, ):
        outputs = []
        for fname in os.listdir(asset_type):
            if fname.endswith(_from):
                raw_data = __compile(asset_type,  fname)
                # Avoid including the output twice. Hint bake, by adding a _ filename convention
                new_filename = "_" + fname.replace(_from, _to)
                open(asset_type + os.sep + new_filename, 'w').write(raw_data)
                outputs.append((raw_data, new_filename))
        return outputs

    return _compile


def load_content(config):
    """Pre-process and load each asset type into a dict and return a tuple of such dicts"""

    # Compile HAML
    _haml = {fname: compiled_out for compiled_out, fname in compile_assets(config, 'templates')(_compile_haml, 'haml', 'html')}
    _html = load_assets(config)('templates', 'html')
    templates = __newdict(_html, _haml)

    # Compile SCSS
    _scss = {fname: compiled_out for compiled_out, fname in compile_assets(config, 'styles')(_compile_scss, 'scss', 'css')}
    _css = load_assets(config)('styles', 'css')
    styles = __newdict(_css, _scss)

    # Compile Coffeescript
    _cs = {fname: compiled_out for compiled_out, fname in compile_assets(config, 'scripts')(_compile_coffee, 'coffee', 'js')}
    _js = load_assets(config)('scripts', 'js')
    scripts = __newdict(_js, _cs)

    # All Posts
    posts = load_posts(config)

    return templates, styles, scripts, posts


def bake(config, templates, posts, styles, scripts, recipes, minify=False):
    """Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS
       NOTE: This function modifies 'posts' dictionary by adding a new posts['html'] element"""
    for post in posts:
        converted_html = _markstache(config, post, _get_template_path(templates, post[
            'template']), recipes=recipes)  # each post can have its own template
        post['html'] = converted_html

    _params = {}

    if minify:
        print "Minifying CSS/JS"
        _params = {"style_sheet": cssmin.cssmin("".join(styles.values())),
                "script": jsmin.jsmin("".join(scripts.values())),
                "json_data": json.dumps(posts),
                "relative_path": config['relative_path'],
                "title": config['title']
                }
    else:
        _params = {"style_sheet": "".join(styles.values()),
                "script": "".join(scripts.values()),
                "json_data": json.dumps(posts),
                "relative_path": config['relative_path'],
                "title": config['title']
                }

    _params.update(recipes)
    return pystache.render(templates['index.mustache.html'], _params)



def _get_template_path(templates, post_template_name):
    if post_template_name.endswith(".haml"):
        key = "_" + post_template_name.replace(".haml", ".html")
        return templates[key]
    else:
        return templates[post_template_name]


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


def _markstache(config, post, template, recipes=None):
    """Converts Markdown/Mustache/YAML to HTML."""
    html_md = md.markdown(post['body'].decode("utf-8"))
    _params = __newdict(post, {'body': html_md})
    _params.update(recipes) if recipes else None
    return pystache.render(template, _params)


def _compile_haml(asset_type, fname):
    return hamlpy.Compiler().process(_read(fname, asset_type))


def _compile_scss(asset_type, fname):
    return Scss().compile(_read(fname, asset_type))


def _compile_coffee(asset_type, fname):
    return coffeescript.compile(_read(fname, asset_type))


def _format_date(fname):
    return datetime.strptime(time.ctime(os.path.getmtime(fname)), "%a %b %d %H:%M:%S %Y").strftime("%m-%d-%y")


def _recipes():
    return [f.strip('.py') for f in os.listdir('recipes') if f.endswith('py') and not f.startswith("__")]


def __newdict(*dicts):
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict


def main(config_path, minify=False):
    """Let's cook an Apple Pie"""
    config = load_config(config_path)
    templates, styles, scripts, posts = load_content(config)
    recipes = load_recipes(config)
    output = bake(config, templates, posts, styles, scripts, recipes, minify=minify)
    open('index.html', 'w').write(output)
    print 'Generated index.html'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="+", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yaml"])
    args = parser.parse_args(sys.argv[1:])
    __config_path = args.config[0]
    minify = False
    serve = False
    if "min" in args.string_options: minify = True
    if "serve" in args.string_options: serve = True
    print "Using config from " + __config_path
    main(__config_path, minify=minify)

    if serve:
        pipe_git = Popen(['git', 'branch'], stdout=PIPE, stderr=PIPE, stdin=PIPE)
        branches = pipe_git.stdout.read()
        if not re.search("gh-pages\n", branches):
            os.system("git branch gh-pages")
        os.system("git stash")
        time.sleep(1)
        os.system("cp index.html /tmp")
        os.system("git checkout gh-pages")
        time.sleep(1)
        os.system("cp /tmp/index.html index.html")
        time.sleep(1)
        os.system("git add index.html")
        time.sleep(1)
        os.system("git commit -m \"new index.html\"")
        time.sleep(1)
        os.system("git push origin gh-pages")
        time.sleep(1)
        os.system("git checkout master")
        time.sleep(1)
        os.system("git stash pop")

