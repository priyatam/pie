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
import coffeescript
import recipes


def load_config(config_path):
    """Loads configuration from config.yaml"""
    with open(config_path, "r") as fin:
        return yaml.load(fin.read())


def load_assets(config):
    """Loads assets as raw content into a dictionary, looked up by its fname.
    Closure accepts an asset_type ('templates', 'styles', 'posts', 'scripts') and a filter that filters based on file ext"""
    return lambda asset_type, filter: {fname: _read(fname, asset_type) for fname in os.listdir(asset_type) if fname.endswith(filter) and not fname.startswith("_")}


def load_recipes():
    recipe_defs = dir(recipes)
    recipes_dict = {}
    for recipe_def in recipe_defs:
        if not recipe_def.startswith("__"):
            current_def = getattr(recipes, recipe_def)
            recipes_dict.update({recipe_def: current_def})
    return recipes_dict


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
                "modified_date": _format_date(fname)
            }
            post.update(yaml_data)  # Merge Yaml data for future lookup
            posts.append(post)
        else:
            print """Filename format: ['a/A', 2.5, '_', '.', '-', '~']"""
            exit(1)

    return posts


def compile_assets(config, asset_type):
    """Compiles asset types: css, js, html using pre-processors.
       Currently supports haml, scss, coffeescript."""
    def _compile(__compile, _from, _to,):
        outputs = []
        for fname in os.listdir(asset_type):
            if fname.endswith(_from):
                raw_data = __compile(asset_type, fname)  # Inner Closure (__compile) applying on outer closure (_compile)
                new_filename = "_" + fname.replace(_from, _to)
                open( asset_type + os.sep + new_filename, 'w').write(raw_data)
                # next run of bake.py will include the output twice.
                # hence the _ convention
                outputs.append((raw_data, new_filename))
        return outputs
    return _compile


def load_content(config):
    """Pre-process and load each asset type into a dict and return a tuple of such dicts"""
    # Compile HAML Templates
    haml_html = {fname: compiled_output for compiled_output, fname in compile_assets(config, 'templates')(_compile_haml, 'haml','html')}
    time.sleep(1) # else, next guy won't see the new file
    templates_css = load_assets(config)('templates', 'html')
    templates = __newdict(templates_css, haml_html)

    # Compile SCSS
    scss_css = {fname: compiled_output for compiled_output, fname in compile_assets(config, 'styles')(_compile_scss, 'scss','css') }
    css_styles = load_assets(config)('styles', 'css')
    styles = __newdict(css_styles, scss_css)

    coffeescripts = {fname: compiled_output for compiled_output, fname in compile_assets(config, 'scripts')(_compile_coffee, 'coffee','js') }
    js_scripts = load_assets(config)('scripts', 'js')
    scripts = __newdict(js_scripts, coffeescripts)

    posts = load_posts(config)

    return templates, styles, scripts, posts


def bake(config, templates, posts, styles, scripts):
    """Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS
       NOTE: This function modifies 'posts' dictionary by adding a new posts['html'] element"""
    for post in posts:
        converted_html = _markstache(post, _get_template_path(templates, post['template']))  # each post can have its own template
        post['html'] = converted_html

    style_sheets = styles.values()
    style_sheet = "".join(style_sheets)
    scripts = scripts.values()
    script = "".join(scripts)
    content = pystache.render(templates['index.mustache.html'],
                              {"style_sheet": style_sheet,
                               "script": script,
                               "json_data": json.dumps(posts), "relative_path": config['relative_path'],
                               "title": config['title']
                               })
    return content


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


def _markstache(post, template):
    """Converts Markdown/Mustache/YAML to HTML."""
    html_md = md.markdown(post['body'].decode("utf-8"))
    _params = __newdict(post, {'body': html_md})
    recipes_dict = load_recipes()
    _params.update(recipes_dict)
    return pystache.render(template, _params)


def _compile_haml(asset_type, fname):
    return hamlpy.Compiler().process(_read(fname, asset_type))


def _compile_scss(asset_type, fname):
    return Scss().compile(_read(fname, asset_type))


def _compile_coffee(asset_type, fname):
    return coffeescript.compile(_read(fname, asset_type))


def _format_date(fname):
    """Returns a formatted fname.date"""
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
    output = bake(config, templates, posts, styles, scripts)
    print output


if __name__ == '__main__':
    __config_path = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    main(__config_path)
