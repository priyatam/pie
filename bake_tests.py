#!/usr/bin/env python

'''
$ env TEST=yes python bake_tests.py
'''

import unittest
import types
import bake


class BakeTests(unittest.TestCase):
    def setUp(self):
        self.config_path = "./config.yaml"
        self.config = bake.load_config(self.config_path)

    def test_load_config(self):
        self.assertEqual(types.DictType, type(self.config))

        self.assertEqual(2, len(self.config['templates']))
        self.assertEqual(2, len(self.config['styles']))
        self.assertEqual(1, len(self.config['scripts']))
        self.assertEqual('/index.html', self.config['relative_path'])

    def test_load_assets(self):
        templates = bake.load_assets(self.config)('templates', 'haml')
        self.assertEqual(types.DictType, type(templates))
        self.assertIsNotNone(templates['post.mustache.haml'])

    def test_load_posts(self):
        posts = bake.load_contents(self.config)
        self.assertEqual(2, len(posts))
        self.assertIsNotNone(posts[0]['body'])

    def test_load_content(self):
        templates, styles, scripts, posts = bake.load_recipes(self.config)
        self.assertEqual(types.DictType, type(templates))
        self.assertEqual(types.DictType, type(styles))
        self.assertEqual(types.DictType, type(scripts))
        self.assertEqual(types.ListType, type(posts))
        for post in posts:
            self.assertEqual(types.DictType, type(post))

        for k, v in templates.items():
            self.assertIsNotNone(k in self.config.values())
            self.assertIsNotNone(v)
        for k, v in styles.items():
            self.assertIsNotNone(k in self.config.values())
            self.assertIsNotNone(v)
        for k, v in scripts.items():
            self.assertIsNotNone(k in self.config.values())
            self.assertIsNotNone(v)

    def bake(self):
        pass

    def test_read(self):
        fin = bake._read('bake_tests.py', '.')
        self.assertTrue('import unittest' in fin)

    def test_read_posts(self):
        yaml, post = bake._read_yaml('posts', 'introduction.md')
        self.assertEqual(5, len(yaml))
        self.assertIsNotNone(post)

    def test_markstache(self):
        post = {'body': """#What's the point of another static generator ?
                            It's a *single file* static generator with all the bells and whistles.
                            Write all your md posts in posts. Your file name becomes the url.
                        """
        }
        template = """ <div class="post">
                            {{{ body }}}
                        </div>
        """
        stache = bake._markstache(post, template)
        self.assertIsNotNone(stache)

    def test__format_date(self):
        dt = bake._format_date('bake_tests.py', 'c')
        self.assertIsNotNone(dt)


if __name__ == '__main__':
    unittest.main()
