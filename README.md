# Literary publishing, for humans

Thousands of poems in the public domain live buried in websites. Hundreds of literary magazines archive thousands more that go undiscovered. Humans, even machines, can't search them in a central library.

Enter Literatte: A mobile-first, literary publishing toolkit that can print itself and fit in your **dropbox**.

Literatte: A mobile-first, literary publishing toolkit that fits in your **dropbox**.

## Overview

Most cms platforms today are blog and database centric like wordpress, drupal, tumblr, even weebly: platforms where users drag and drop designs with **content buried in code**. Designs are coupled with cms, content _can't_ be read outside them. Designing websites around a 'cms' locks you in with a toolkit, an online service, an agency charging your money for no real value.

Static site generators, jekyll, middleman, and over [a hundred variations](http://nanoc.ws/about/) of the same idea, simplify website development by an order of magnitude, replacing databases with filesystems and promoting Markdown over editors. However, you have to be a developer to customize them.

We can go one step further: editors and publishers should be able to write templates by hand, buy reusable themes, add, edit content, **script an editorial workflow**, and host a site on dropbox. No lock-ins, no contracting agencies, no cms.

## Usage

Note: The current steps are still developer-centric. Human api will be available soon.

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

This work is being done in parallel to Poetroid, an open platform to discover poetry together with a unified [api](http://en.wikipedia.org/wiki/Application_programming_interface). Poetroid is currently used internally by our editors for [curating poems from the public domain](https://github.com/Facjure/poetroid-public-domain).

## Documentation

Coming soon.

## Contributers

- Priyatam Mudivarti: writer, engineer, and founder of Facjure LLC
- Sreeharsha Mudivarti: musician, engineer, and survivor of a space ship crash.

If you're a web developer and wants to move litarature forward, help, send a pull request!

## Copyright & License

Copyright (c) Facjure LLC. All rights reserved.

The use and distribution terms for this software are covered by [Eclipse Plugin License v 1.0](http://opensource.org/licenses/eclipse-1.0.php), which can be found in the file LICENSE at the root of this distribution.

By using this software in any fashion, you are agreeing to be bound by the terms of this license. You must not remove this notice, or any other, from this software.
