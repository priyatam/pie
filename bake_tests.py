#!/usr/bin/env python

'''
./bake_tests.py
'''

import unittest
import types
import bake
from pieutils import *


class BakeTests(unittest.TestCase):
    def setUp(self):
        self.config_path = "./config.test.yml"
        self.config = load_config(self.config_path)

    def test_load_config(self):
        self.assertEqual(types.DictType, type(self.config))
        self.assertEqual("https://github.com/Facjure/frozen-pie", self.config['github_repo'])

    def test_load_contents(self):
        posts = bake.load_contents(self.config)
        for post in posts:
            self.assertEqual(types.DictType, type(post))
        self.assertEqual(8, len(posts))
        self.assertIsNotNone(posts[0]['body'])

    def test_load_recipes(self):
        style, script, lambdas = bake.load_recipes(self.config)
#        self.assertEqual(types.UnicodeType, type(style))
#        self.assertEqual(types.UnicodeType, type(script))
        self.assertEqual(types.DictType, type(lambdas))
        self.assertIsNotNone(style)
        self.assertIsNotNone(script)
        for k, v in lambdas.items():
            self.assertIsNotNone(v)

    def testread(self):
        fin = read('bake_tests.py', '.')
        self.assertTrue('import unittest' in fin)

    def test_read_posts(self):
        yaml, post = read_yaml('content', 'introduction.md')
        self.assertEqual(6, len(yaml))
        self.assertIsNotNone(post)

    def test_markstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post.mustache"
        stache = bake._markstache(self.config, post, template_name)
        self.assertIsNotNone(stache)

    def test_textstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
                }

        template_name = "post_plain.mustache"
        stache = bake._textstache(self.config, post, template_name)
        self.assertIsNotNone(stache)

    def test_format_date(self):
        dt = bake.format_date('bake_tests.py')
        self.assertIsNotNone(dt)


if __name__ == '__main__':
    unittest.main()
