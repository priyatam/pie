#!/usr/bin/env python

'''
$ env TEST=yes python bake_tests.py
'''

import unittest
import types
import bake


class BakeTests(unittest.TestCase):

    def setUp(self):
        """ """

    def test_load_config(self):
        config = bake.load_config()
        self.assertEqual(types.DictType, type(config))
         
        self.assertEqual(2, len(config['templates']))
        self.assertEqual(1, len(config['styles']))
        self.assertEqual(1, len(config['scripts']))
        self.assertEqual('/index.html', config['relative_path'])

    def test_load_content(self):
        config = {'templates': ['post.mustache', 'index.mustache'], 'scripts': ['index.js'], 'styles':['index.css'], 'relative_path': ['/index.html']}
        content = bake.load_content(config)
        self.assertEqual(types.DictType, type(content))
        for k, v in content.items(): 
            self.assertIsNotNone(k in config.values())            
            self.assertIsNotNone(v)            
           
    
if __name__ == '__main__':
    unittest.main()
