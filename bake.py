#!/usr/bin/env python
"""
Usage:
python bake.py > index.html

Algo:
Read config.yaml
For each post, generate complete html by applying Mustache templates
Generate index.html with included CSS, JS

"""

import os, time
import yaml, markdown as md, pystache
import json

def load_config():
    """Loads configuration from config.yaml"""
    with open("config.yaml", "r") as fin:
        return yaml.load(fin.read())


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    posts = []
    for fname in os.listdir("posts"):
        yaml_data, md_data = read_markdown('posts', fname)
        fname = 'posts' + os.sep + fname
        post = {
            "name": fname,
            "body": md_data, # raw, unprocessed md
            "created_date": time.ctime(os.path.getmtime(fname)),
            "modified_date": time.ctime(os.path.getctime(fname))
        }
        post.update(yaml_data)  # Merge Yaml data
        posts.append(post)

    return posts


def load_layout(config):
    """Reads templates, scripts, styles and stores them as dictionaries"""
    content = {}
    # Group these by type in config
    templates = rawcontent_by_fname(config, 'templates')
    styles = rawcontent_by_fname(config, 'styles')
    scripts = rawcontent_by_fname(config, 'scripts')
    # Merge them
    content.update(templates)
    content.update(styles)
    content.update(scripts)

    return content


def rawcontent_by_fname(config, key):
    """Creates a dictionary of fname->raw_content, where raw_content is config(key)"""
    return {fname: read(key, fname) for fname in config[key]}


def read(subdir, fname):
    """Reads subdir/<fname> as raw content"""
    with open(subdir + os.sep + fname, "r") as fin:
        return fin.read()


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
    raw_md = md.markdown(post['body'])
    return pystache.render(template, {"body": raw_md})


def bake(config, content, posts):
    """ Parse everything. Wrap results in a final page in Html5, CSS, JS, POSTS """
    # Stache
    for post in posts:
        post['html'] = markstache(post, content[post['template']])
    
    # Merge into one
    output = pystache.render(content['index.mustache'],
                             {"style_sheet": content['index.css'], "script": content['index.js'],
                              "json_data": json.dumps(posts), "relative_path": config['relative_path']})
    print output


def main():
    """Let's cook an Apple Pie"""
    config = load_config()
    content = load_layout(config)
    posts = load_posts(config)
    bake(config, content, posts)


if __name__ == '__main__':
    main()
