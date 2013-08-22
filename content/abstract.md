---
title: Abstract
type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 08-10-13
---

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery


How do you write content once, pick any design, logic, and template, and compose a website with minimal hosting requirements? How do you do this without any framework, toolkit, or platform lock-in?

To understand this we must look at how we build websites. Most content platforms today are blog and CMS centric like Wordpress, Drupal, Tumblr, Weebly, and platforms where users drag and drop designs with content buried in code. Designs they _can't_ control. Content that they _can't_ read outside the tool. Designing websites around these 'platforms' means you are locked in to their workflow, updates, trapped in a black box. Static site generators like Jekyll, Middleman, DocPad, and over [a hundred variations](http://nanoc.ws/about/) toolkits simplify website development by an order of magnitude. They're built for developers and designers who like to hack and take control to build the whole site, independently, in one go. 

This is great, except they break a simple rule: **Coupling**. They couple at least two of the following: _authors, designers, developers, hosting providers_. Logic is mixed in with Templates, Styles are tied to Templates, and Plugins—that extend your website—are not portable across toolkits, not even the same language. When you add up developers using these toolkits, you end up with millions of lines of code and content and design that aren't compatible with each other. 

Things shouldn’t be this way. Not in 2013.
