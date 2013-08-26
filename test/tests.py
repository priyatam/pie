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

    def test_read(self):
        fin = read('tests.py', '.')
        assert 'import unittest' in fin

    def test_read_yaml(self):
        pass

    def test_format_date(self):
        dt = bake.format_date('tests.py')
        assert dt != None


class TestBake:

    def setup(self):
        self.config_path = "config.test.yml"
        self.config = load_config(self.config_path)

    def test_load_contents(self):
        posts = bake.load_contents(self.config)
        for post in posts:
            assert types.DictType == type(post)
        assert 8 == len(posts)
        assert posts[0]['body'] != None

    def test_load_dynamic_templates(self):
        pass

    def test_load_lambdas(self):
        pass


    def test_load_recipes(self):
        style, script, lambdas = bake.load_recipes(self.config, [], [])
        assert types.UnicodeType == type(style)
        assert types.UnicodeType == type(script)
        assert types.DictType == type(lambdas)
        assert style != None
        assert script != None
        for k, v in lambdas.items():
            assert v != None


    def test_read_posts(self):
        yaml, post = read_yaml('../content', 'abstract.md')
        assert 5 == len(yaml)
        assert post != None

    def test_bake_contents(self):
        pass

    def test_bake_dynamic_templates(self):
        pass

    def test_markstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post.mustache"
        stache = bake._markstache(self.config, post, template_name)
        assert stache != None

    def test_textstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post_plain.mustache"
        stache = bake._textstache(self.config, post, template_name)
        assert stache != None

    def test_compile_scss(self):
        pass

    def test_get_lambdas(self):
        pass

    def test_cook(self):
        pass

def main():
    pytest.main("tests.py")
