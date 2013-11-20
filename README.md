# Publish Literary Magazines, Together

Hundreds of magazines and indie publishers publish their literature on print, or bury their word and pdfs in a cms, yet we don't have access to read, edit, and discover them, like machines.

Let's build one.

## Overview

Most cms platforms today are blog and database centric like wordpress, drupal, tumblr, even weebly: platforms where users drag and drop designs with **content buried in code**. Designs are coupled with cms, content _can't_ be read outside them. Designing websites around a 'cms' locks you in with a programmer, an agency, a software company that doesn't understand literature.

Static site generators, on the other hand, simplify website development by an order of magnitude by replacing databases with filesystems. Opensource frameworks like jekyll, middleman, and over [a hundred variations](http://nanoc.ws/about/) of the same idea are excellent, but they're still built for developers, not indie publishers.

Things shouldn’t be this way. Not in 2013.

Publishers should be able to write templates, buy themes, script an editorial workflow and host a site on dropbox. No lock-ins, no cms, no contracting agencies, and still be able to hire an engineer for one-off complex tasks.

## Usage

TODO: Currently developer-centric steps.

Setup:

    $ mkvirtualenv pie
    $ pip install -r requirements.txt

Run:

    $ cd pie
    $ python pie.py

Tests:

    $ cd pie-test
    $ py.test test/tests.py

## Status and Roadmap

Not stable. Currently in *Research & Development*.

This work is being done in parallel to Poetroid, an open platform to discover poetry together with a unified [api](http://en.wikipedia.org/wiki/Application_programming_interface) for web, mobile, and print. Poetroid is currently used internally by our editors for [curating poems from the public domain](https://github.com/Facjure/poetroid-public-domain).

## Documentation

Coming soon.

## Copyright & License

Copyright (c) Facjure LLC. All rights reserved.

The use and distribution terms for this software are covered by [Eclipse Plugin License v 1.0](http://opensource.org/licenses/eclipse-1.0.php), which can be found in the file LICENSE at the root of this distribution.

By using this software in any fashion, you are agreeing to be bound by the terms of this license. You must not remove this notice, or any other, from this software.
