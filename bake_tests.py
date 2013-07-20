#!/usr/bin/env python

'''
$ env TEST=yes python bake_tests.py
'''

import unittest
import types
import bake


class BakeTests(unittest.TestCase):
    def setUp(self):
        self.config = {'templates': ['post.mustache', 'index.mustache'], 'scripts': ['index.js'],
                       'styles': ['index.css'], 'relative_path': ['/index.html']}

    
    def test_load_config(self):
        config = bake.load_config()
        self.assertEqual(types.DictType, type(config))

        self.assertEqual(2, len(config['templates']))
        self.assertEqual(1, len(config['styles']))
        self.assertEqual(1, len(config['scripts']))
        self.assertEqual('/index.html', config['relative_path'])


    def test_load_layout(self):
        content = bake.load_layout(self.config)
        self.assertEqual(types.DictType, type(content))
        for k, v in content.items():
            self.assertIsNotNone(k in self.config.values())
            self.assertIsNotNone(v)


    def test_read_markdown(self):
        yaml, post = bake.read_markdown('posts', 'page.md')
        self.assertEqual(5, len(yaml))
        self.assertIsNotNone(post)

   
    def test_load_posts(self):
        posts = bake.load_posts(self.config)
        self.assertEqual(2, len(posts))
        self.assertIsNotNone(posts[0]['body'])

  
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
        stache = bake.markstache(post, template)
        self.assertIsNotNone(stache)
 
    def bake(self):
        pass #TODO
        
if __name__ == '__main__':
    unittest.main()
