---
title: Tech
_type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 07-21-13
---

### How?

Toolkit is built in Python using functional programming. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel.

SammyJs will be used to create a single page.

**Content** can be anything: blog-post, page, navigation, header, footer, wiki, sitemap, etc., The type can be identified by reading the content's metadata.

**Template** accepts content with same type. For example a user should be able to take a _blog_ content and stick it into any _blog_ template. He can't, however, stick a _home_ content into a _nav_ template.

**Style** breathes life into Templates. They can be written in CSS3, or compiled from LESS, SCSS, Bourbon.

**Recipe** is nothing but a package of Templates, Styles, and Lambdas under a single namespace.

**Lambdas** are logic written in any language that supports functional concepts like Javascript, Coffeescript, Clojurescript on the browser, or Python on the serverside.



