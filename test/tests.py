#!/usr/bin/env python
import pytest
import types
import bake
import pieutils
from pieutils import *

pieutils.logger = get_logger()


class TestPieUtils:

    def setup(self):
        self.config_path = "config.test.yml"

    def test_load_config(self):
        config = load_config(self.config_path)
        assert types.DictType == type(config)
        assert "https://github.com/Facjure/frozen-pie" == config['github_repo']
        with pytest.raises(SystemExit):
            load_config("./config.test.bad.yml")

    def test_format_date(self):
        dt = format_date('tests.py')
        assert dt != None
        assert "13" in dt

    def test_read(self):
        fin = read('tests.py', '.')
        assert 'import unittest' in fin

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
        self.config_path = "config.test.yml"
        self.config = load_config(self.config_path)

    def test_read_posts(self):
        yaml, post = read_yaml('content', 'abstract.md')
        assert 5 == len(yaml)
        assert post != None

    def test_load_contents(self):
        posts = bake.load_contents(self.config)
        for post in posts:
            assert types.DictType == type(post)
        assert 2 == len(posts)
        assert posts[0]['body'] != None
        assert u"Antoine de Saint-Exupery" in posts[0]['body']

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
        assert "display" in style
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

    def test_compile_asset(self):
        _styles_path = self.config["recipe_root"] + os.sep + "styles"
        compiled_sheet = bake.compile_asset(self.config, _styles_path, "styles.scss")(bake._compile_scss, 'scss', 'css')
        assert compiled_sheet != None
        assert "display" in compiled_sheet

    def test_compile_scss(self):
        compiled_css = bake._compile_scss(self.config)
        assert compiled_css != None
        assert "display" in compiled_css

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

def main():
    pytest.main("tests.py")
