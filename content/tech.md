---
title: Spec
type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 07-16-13
---

**Implementing the Spec**

**Content** can be anything: blog-post, page, navigation, header, footer, wiki, sitemap, etc., The type can be identified by reading the content's metadata.

**Template** accepts content with same type. For example a user should be able to take a _blog_ content and stick it into any _blog_ template. He can't, however, stick a _home_ content into a _nav_ template.

**Style** breathes life into Templates. They can be written in CSS3, or compiled from LESS, SCSS, Bourbon.

**Recipe** is nothing but a package of Templates, Styles, and Lambdas under a single namespace.

**Lambdas** are logic written in any language that supports functional concepts like Javascript, Coffeescript, Clojurescript on the browser, or Python on the serverside.

SammyJs will be used to create a single page.

Toolkit is built in Python using functional programming. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel.

**Ten Coding Rules**

1. Forget classes, compose in functions, think of modules, namespaces
2. Everything is a Dictionary, List, or Set
3. No strage loops: Comprehensions are your friends
4. No Global variables, use only pure functions
5. Functions can return tuples; use them freely
6. Compose, Reuse, Refactor = Simple, Simpler, Simplicity
7. Forget databases
8. Be open, be flexible, remember to curate good practices
9. If you run out of gas, there's always Clojure
10. Eat your own pie
