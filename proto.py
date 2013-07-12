'''
Just Testing Markdown, YAML, Pystache

'''

import pystache
import yaml
from markdown import Markdown

text = ''' Hi **{{person}}** ! '''
yaml_data = ''' person: name '''

## First, process md
md = Markdown(extensions=['nl2br'], output_format="html5")
stash_html = md.convert(text)
print stash_html

## Then, process Mustache with YAML to final Html5
print yaml.load(yaml_data)
html = pystache.render(stash_html, yaml.load(yaml_data))

## Yay
print html

