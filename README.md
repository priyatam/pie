# Frozen Pie

<img src="https://secure.travis-ci.org/Facjure/frozen-pie.png?branch=master" style="max-width:100%;">

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery

## Overview

How do you design a website for semantic HTML 5 content? 

Current platforms are Blog and CMS centric: Drupal, Wordpress, Tumblr, Weebly, Jekyll, Middleman, etc. They are great for developers or users who want to click and push, however, these solutions break a simple rule: _Coupling_.

They couple at least two of the following: authors, designers, developers, hosting. Their styles are not compatible across platforms, across frameworks. When you upgrade some plugins break, blow on your face. Designs, though in CSS, seem coupled to classes and ids tied to the toolkit beneath; you can't port designs--you can't even move **Content** from one thing to another.

Things shouldn’t be this way.

## Three principles

1. Content is King
2. Design once, View anywhere
3. Logic should be declarative, composed of single tasks

## How it works

Author = Cook

create_crust
> Cook creates content in Markdown/Plain Text with YAML meta-data. A content can be anything.

put_in_pan and add filling
> Designers create generic Templates with Mustache, and optionally, 3rd-party logic (Mustache lambdas), and package them as 'Recipes'.

add_recipes
> Cook selects Recipes

bake_in_oven
> Cook heats everything into a single index.html

serve
> Cook serves the single page to anywhere: github pages, S3, dreamhost, email, etc.,

It's time we give them power.

## Documentation
A minimalist website builder for semantic content with an emphasis on Plain Text, Markdown, Mustache Templates, Mustache Lambdas,  HTML 5, and Responsive Web Design. For more info, see the [Wiki](https://github.com/Facjure/frozen-pie/wiki).

## Status
Unstable, under active development.

## Copyright and License
Copyright 2013 Facjure LLC,  under the Apache 2.0 License.
