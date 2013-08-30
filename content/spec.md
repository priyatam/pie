---
title: Spec
_type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 07-16-13
---

###  How does it work?

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


### Explain please ...

**Content** can be anything: blog-post, page, navigation, header, footer, wiki, sitemap, etc., The type can be identified by reading the content's metadata.

**Template** accepts content with same type. For example a user should be able to take a _blog_ content and stick it into any _blog_ template. He can't, however, stick a _home_ content into a _nav_ template.

**Style** breathes life into Templates. They can be written in CSS3, or compiled from LESS, SCSS, Bourbon.

**Recipe** is nothing but a package of Templates, Styles, and Lambdas under a single namespace.

**Lambdas** are logic written in any language that supports functional concepts like Javascript, Coffeescript, Clojurescript on the browser, or Python on the serverside.

SammyJs will be used to create a single page.

Toolkit is built in Python using functional programming. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel.
