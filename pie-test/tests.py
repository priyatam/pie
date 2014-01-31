#!/usr/bin/env python
"""
Can only be run from the parent directory as,
> py.test test/tests.py
"""
import os
import sys
owd = os.getcwd()
root_path = owd + "/demos/site-with-blog"
sys.path.append(owd)
os.chdir("pie-test")

import pytest
import types
import pie.pie as pie
import pie.contents as contents
import pie.templates as templates
from pie.utils import *

pie.logger =  get_logger()

class TestPieUtils:

    def setup(self):
        self.content_path = "content"

    def test_load_config(self):
        config = load_config(root_path, self.content_path)
        assert types.DictType == type(config)

    def test_read(self):
        fin = read('tests.py', '.')
        assert 'import pytest' in fin

    def test_read_yaml(self, tmpdir):
        tmp_file = tmpdir.join("test.yml")
        tmp_file.write('''---
foo: bar
---
'''
)
        yaml, content = read_yaml(tmpdir.strpath, "test.yml")
        assert yaml['foo'] == "bar"
        assert content == u""


class TestBake:

    def setup(self):
        self.content_path = "content"
        self.config = load_config(root_path, self.content_path)

    def test_read_posts(self):
        yaml, post = read_yaml('content', 'abstract.md')
        assert 5 == len(yaml)
        assert post != None

    def test_load_contents(self):
        posts = contents.load(self.config)
        for post in posts:
            assert types.DictType == type(post)
        assert 1 == len(posts)
        assert posts[0]['body'] != None


    def test_load_dynamic_templates(self):
        templates = bake.load_dynamic_templates(self.config)
        for template in templates:
            assert types.DictType == type(template)
        assert 1 == len(templates)
        assert templates[0]['body'] != None
        assert u"{{#posts}}" in templates[0]['body']

    def test_load_lambdas(self):
        contents = bake.load_contents(self.config)
        dynamic_templates = bake.load_dynamic_templates(self.config)
        lambdas = bake.load_lambdas(self.config, contents, dynamic_templates)
        for k,v in lambdas.items():
            assert types.FunctionType == type(v)
        assert len(lambdas) == 2

    def test_load_recipes(self):
        contents = bake.load_contents(self.config)
        dynamic_templates = bake.load_dynamic_templates(self.config)
        style, script, lambdas = bake.load_recipes(self.config, contents, dynamic_templates)
        assert types.UnicodeType == type(style)
        assert types.UnicodeType == type(script)
        assert types.DictType == type(lambdas)
        assert style != None
        assert script != None
        assert "width" in style
        assert "sammy" in script
        for k,v in lambdas.items():
            assert types.FunctionType == type(v)
        assert len(lambdas) == 2


    def test_bake_contents(self):
        contents = bake.load_contents(self.config)
        dynamic_templates = bake.load_dynamic_templates(self.config)
        lambdas = bake.load_lambdas(self.config, contents, dynamic_templates)
        bake.bake_contents(self.config, contents, lambdas)
        for content in contents:
            assert "html" in content
            assert content["html"] != None

    def test_bake_dynamic_templates(self):
        contents = bake.load_contents(self.config)
        dynamic_templates = bake.load_dynamic_templates(self.config)
        lambdas = bake.load_lambdas(self.config, contents, dynamic_templates)
        bake.bake_dynamic_templates(self.config, dynamic_templates, lambdas)
        for template in dynamic_templates:
            assert "html" in template
            assert template["html"] != None

    def test_markstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post.mustache"
        stache = bake._markstache(self.config, post, template_name)
        assert stache != None
        assert "<h1>What's the point of another static generator ?" in stache

    def test_htmlstache(self):
        meta, template = read_yaml(self.config["templates_path"], "blog.mustache")
        contents = bake.load_contents(self.config)
        dynamic_templates = bake.load_dynamic_templates(self.config)
        lambdas = bake.load_lambdas(self.config, contents, dynamic_templates)
        stache = bake._htmlstache(self.config, template, lambdas=lambdas)
        assert stache != None
        assert "plain_text" in stache

    def test_textstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post_plain.mustache"
        stache = bake._textstache(self.config, post, template_name)
        assert stache != None
        assert "#What's the point of another static generator ?" in stache

    def test_get_lambda_module_namess(self):
        modules = bake._get_lambda_module_names(self.config)
        assert len(modules) == 1
        assert modules[0] == 'default'

    def test_cook(self):
        pie = bake.cook(self.config)
        assert pie != None
        assert "<style" in pie
        assert "<script>" in pie
        assert "<nav" in pie
        assert self.config["title"] in pie
        assert self.config["github_repo"] in pie

