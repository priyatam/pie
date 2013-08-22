---
title: Abstract
type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 08-10-13
---
> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery


What is Content and Design freedom?

To understand this, we must look back at how we build websites today. Current content platforms are CMS centric like Wordpress, Drupal, Tumblr, Weebly which are good for users who want to click and drag and drop designs and logic. Design they can't control. Logic that they can't write themselves. Designing websites around these 'platforms' means you are locked in to their platforms. The other, more newer platforms, are static site generators like Jekyll, Middleman, DocPad etc., They are built for developers and designers who like to hack, who like to take complete control and build the whole thing in one go.

Both approaches break a simple rule: **Coupling**. They couple at least two of the following: _authors, designers, developers, hosting providers_.

Their styles are not compatible across frameworks. CSS styles are coupled to classes and ids of the underlying templates and toolkits. You can't port designs, you can't even move content from one platform to another without hacking your way through scripts and xml export hell. When you upgrade, some plugins break, blowing on your face. Everything is locked to a framework, a language, _leaving content behind_. Imagine moving from Wordpress to Tumblr, or Tumblr to a custom Middleman app--imagine moving two hundred blog posts and pages? It's a complete mess. Things shouldn’t be this way.

Not in Python.

Frozen Pie is a minimalist website builder for publishers with an emphasis on Design and Content _freedom_. It's built around specs, rather than frameworks; key specs include [Mustache](http://mustache.github.io), [Markdown](http://daringfireball.net/projects/markdown/) and [Semantic HTML 5](http://diveintohtml5.info/semantics.html). When you build content and design around specs, you have language freedom, platform freedom, decoupled logic that can run anywhere, pure functional programming techniques & &#955; architectures. You can focus on building content that evolves in its own pace.

Principles:

1. Content is King
1. Use any Design
1. Logic is declrative
1. Host anywhere
1. Decouple everything
1. Go back in time
