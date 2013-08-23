---
title: Abstract
type: page
template: page.mustache
author: Priyatam Mudivarti
post_date: 08-10-13
---

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery


How do you write content once, pick any design, logic, template, and compose a website with minimal hosting requirements? How do you build this without any framework, platform, or vendor lock-in?

To understand what can be done, we must look at what _can't_ be done today.

Most content platforms are blog and CMS centric like Wordpress, Drupal, Tumblr, Weebly, and platforms where users drag and drop designs with content buried in code. Designs they _can't_ control. Content that they _can't_ read outside their toolkits. Designing websites around these 'platforms' means you are locked in to their workflow, their language of choice, their opinions, and if you disagree you need a deep understanding of their toolkit—if it's opensource—to hack your way in. Most content publishers can't afford a fulltime cms developer anyway.

Static site generators, on the other hand, simplify website development by an order of magnitude by replacing databases with filesystems, by eliminating complex servers. Frameworks like Jekyll, Middleman, DocPad, and over [a hundred variations](http://nanoc.ws/about/) of the same idea let you get the work done without any server or database. They're built for developers and designers who like to take control of the whole site, independently, in one go. This is great, but they break an important rule: **Coupling**. They couple at least two of the following: _authors, designers, developers, hosting providers_. Logic is mixed in with Templates, Styles are tied to Templates, and Plugins—that extend your website's design or logic—are not portable across toolkits, not even the same language.

When you add up developers and teams using these toolkits, you end up with millions of lines of code, content, and design, all incompatible with each other, only to become obsolete after the _next best thing_.

Things shouldn’t be this way. Not in 2013.

Let's Build Content Together.
