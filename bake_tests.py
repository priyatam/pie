#!/usr/bin/env python

'''\
$ env TEST=yes python bake_tests.py
'''

import unittest
import bake
    
class BakeTests(unittest.TestCase):

    def setUp(self):
        print 'Running Tests ...'   
                       
                       
    def test_load_config(self):
        config = bake.load_config()  
        self.assertEqual(2, len(config['templates']))
        self.assertEqual(1, len(config['styles']))
        self.assertEqual(1, len(config['scripts']))
        self.assertEqual(1, len(config['system']))
        

if __name__ == '__main__':
    unittest.main()
