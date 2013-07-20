#!/usr/bin/env python
"""
Usage:
python bake.py > index.html

Algo:
Read config.yaml
For each post, generate complete html by applying templates
Generate index.html with included CSS

"""

import os, time
import yaml, markdown as md, pystache
import json


def markstache(template, post):
    """Expands Mustache templates from local YAML data and renders Markdown as HTML"""
    raw_md = md.markdown(post['body'])
    return pystache.render(template, {"body": raw_md})


def load_config():
    """Loads configuration from config.yaml"""
    with open("config.yaml", "r") as fin:
        return yaml.load(fin.read())


def load_layout(config):
    """Reads templates, scripts, styles and stores them as dictionaries"""
    
    content = {}
    # Group these by type in config
    templates = dict(config, 'templates')
    styles = dict(config, 'styles')
    scripts = dict(config, 'scripts')
    # Merge them
    content.update(templates)
    content.update(styles)
    content.update(scripts)
     
    return content


def load_posts(config):
    """Creates a dictionary of Post meta data, including body as 'raw content'"""
    
    posts = []    
    for filename in os.listdir("posts"):
        yaml_data, md_data = read_markdown('posts', filename)
        filename = 'posts' + os.sep + filename
        post = {
            "name": filename,
            "body": md_data, # raw, unprocessed md
            "created_date": time.ctime(os.path.getmtime(filename)),
            "modified_date": time.ctime(os.path.getctime(filename))
        }     
        post.update(yaml_data)  # Merge Yaml data
        posts.append(post)        
        
    return posts
    
    
def dict(config, key):
    """Creates a dictionary of key->file (raw content)"""
    return {filename: read(key, filename) for filename in config[key]}


def read(subdir, filename):
    """Reads subdir/<filename> as raw content"""
    with open(subdir + os.sep + filename, "r") as fin:
        return fin.read()


def read_markdown(subdir, filename):
    """Splits Markdown file into a tuple of YAML and content"""
    with open(subdir + os.sep + filename, "r") as fin:
        yaml_and_md = fin.read().split('\n---\n')
        if len(yaml_and_md) == 1:
            return {}, yaml_and_md[0]
        else:
            return yaml.load(yaml_and_md[0]), yaml_and_md[1]

def make_crust(content, posts):
    """Parse Markdown, YAML, Mustache"""
    for post in posts:
        post['html'] = markstache(post, content[post['template']]) 
       
    
def main():
    """Let's cook an Apple Pie"""

    config = load_config()
    content = load_layout(config)
    posts = load_posts(config)
    
    make_crust(content, posts)

    

if __name__ == '__main__':
    main()
