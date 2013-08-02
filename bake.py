#!/usr/bin/env python
"""
Usage:
./bake.py

To serve in gh-pages
./bake.py serve

Algo:
Read config.yaml. For each post.md, process YAML, and apply its Mustache-HAML Template, and generate final HTML.
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
    return {funcname: getattr(mod, funcname) for mod in modules for funcname in dir(mod) if not funcname.startswith("__")}


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


def bake(config, templates, posts, styles, scripts, recipes, serve=False):
    """Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS
       NOTE: This function modifies 'posts' dictionary by adding a new posts['html'] element"""
    for post in posts:
        converted_html = _markstache(config, post, _get_template_path(templates, post[
            'template']), recipes=recipes)  # each post can have its own template
        post['html'] = converted_html

    _params = { "relative_path": config['relative_path'],
                "title": config['title'],
                "posts": posts
              }

    if serve:
        print "Minifying CSS/JS"
        _params.update({"style_sheet": cssmin.cssmin("".join(styles.values())),
                        "script": jsmin.jsmin("".join(scripts.values())),
                        "json_data": json.dumps(posts),
                        })
    else:
        _params.update({"style_sheet": "".join(styles.values()),
                        "script": "".join(scripts.values()),
                        "json_data": json.dumps(posts),
                        })

    _params.update(recipes)
    print posts
    return pystache.render(templates['index.mustache.html'], _params)


def serve_github(config, version=None):
    """
    Algo:
        create or replace deploy
        clone gh-pages into deploy
        git commit index.html -m "hash" (deploy/index.html can always be recreated from src hash)
        git push gh-pages
    """
    proc = Popen(['git','config', "--get","remote.origin.url"],stdout=PIPE)
    url = proc.stdout.readline().rstrip("\n")
    os.system("rm -rf build")
    os.system("git clone -b gh-pages " + url + " build")
    os.system("cp deploy/index.html build/")
    os.system("cd build; git add index.html; git commit -m 'new deploy " + datetime.now() + "'; git push --force origin gh-pages")


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


def _funcname(str):
    """To avoud namespace collisions, filename is a prefix to all functions defined in it. Ex: default_hello_world """
    return str.__name__.strip("recipes.") + "_" + str


def __newdict(*dicts):
    _dict = {}
    for d in dicts:
        _dict.update(d)
    return _dict


def main(config_path, serve=False):
    """Let's cook an Apple Pie"""
    config = load_config(config_path)
    templates, styles, scripts, posts = load_content(config)
    recipes = load_recipes(config)
    output = bake(config, templates, posts, styles, scripts, recipes, serve=serve)
    open('deploy/index.html', 'w').write(output)
    print 'Generated index.html'
    if serve:
        serve_github(config)


if __name__ == '__main__':
    # Parse commmand line options
    parser = argparse.ArgumentParser(description='Some options.')
    parser.add_argument('string_options', type=str, nargs="*", default=[])
    parser.add_argument("--config", nargs=1, default=["config.yaml"])
    args = parser.parse_args(sys.argv[1:])
    __config_path = args.config[0]
    serve = False
    if "serve" in args.string_options:
        serve = True
        __config_path = "config.github.yaml"
        try:
            with open(__config_path): pass
        except IOError:
            print 'You need a config.github.yaml for serve.'
            exit(1)
    print "Using config from " + __config_path
    main(__config_path, serve=serve)
