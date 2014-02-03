#!/usr/bin/env python
"""
Can only be run from the parent directory as,
> py.test pie-test/tests.py
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
import pie.lambdas as lambdas
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
        dynamic_templates = templates.load(self.config)
        for template in dynamic_templates:
            assert types.DictType == type(template)
        assert 1 == len(dynamic_templates)
        assert dynamic_templates[0]['name'] == "blog"

    def test_load_lambdas(self):
        contents_data = contents.load(self.config)
        dynamic_templates = templates.load(self.config)
        lambdas_data = lambdas.load(self.config, contents_data, dynamic_templates)
        for k,v in lambdas_data.items():
            assert types.FunctionType == type(v)
        assert len(lambdas_data) == 2

    def test_mix(self):
        style, script = pie.mix(self.config)
        assert types.UnicodeType == type(style)
        assert types.UnicodeType == type(script)
        assert style != None
        assert script != None
        assert "width" in style
        assert "sammy" in script


    def test_all_bakes(self):
        contents_data = contents.load(self.config)
        dynamic_templates = templates.load(self.config)
        lambdas_data = lambdas.load(self.config, contents_data, dynamic_templates)
        contents.bake(self.config, contents_data, lambdas_data)
        templates.bake(self.config, dynamic_templates, lambdas_data)

        for content in contents_data:
            assert "html" in content
            assert content["html"] != None

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
        stache = templates.to_markstache(self.config, post, template_name)
        assert stache != None
        assert "<h1>What's the point of another static generator ?" in stache

    def test_htmlstache(self):
        contents_data = contents.load(self.config)
        dynamic_templates = templates.load(self.config)
        lambdas_data = lambdas.load(self.config, contents_data, dynamic_templates)
        template = read_yaml(self.config["templates_path"], "blog.mustache")[1]
        stache = templates.to_htmlstache(self.config, template, lambdas=lambdas_data)
        assert stache != None
        assert "Test" in stache

    def test_textstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post.mustache"
        stache = templates.to_textstache(self.config, post, template_name)
        assert stache != None
        assert "#What's the point of another static generator ?" in stache

    def test_bake(self):
        res = pie.bake(self.config, False)
        assert res != None
        assert "<style" in res
        assert "<script>" in res
        assert "<nav" in res
        assert self.config["title"] in res

