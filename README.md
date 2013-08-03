# Frozen Pie

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery

## Abstract
How do you create semantic content and design a website around it? Wordpress? Tumblr? Weebly? Jekyll? Middleman? Custom CMS or handcrafted Sinatra app?

They all break a simple rule: Coupling.

These solutions couple at least two of the following: authors, designers, developers, hosting. Their styles and templates are not compatible with each other, non-portable across frameworks. You can't even move content from one platform to another. 

Things shouldn’t be coupled this way. 

## Three principles

1. Content is King
2. Design once, View anywhere
3. Logic should be declarative, composed of single tasks

Here's a sample workflow:

## How it works

create_crust
> Content creator creates Posts and Pages in Markdown, with optional YAML meta-data

put_in_pan and add filling
> Designers create generic Templates with HAML and Mustache, and optionally, 3rd-party logic (Mustache lambdas), and package them as 'Recipes'.

add_recipes
> Content creator selects Recipes

bake_in_oven
> Content creator runs a script to compile everything into a single index.html

serve
> Content creator runs the script see his/her page live on github pages

## Behind the scenes
Markdown, Mustache, HAML, embracing HTML 5 and CSS3. 

Python with pure functions. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel. Lambdas can be added to analyze inline content with data stored elsewhere. 

Content authors can learn how to run a script, basics of git, Markdown, and that's okay. 

It's time we give them power.

## Documentation
Under active development.

## Status
Under active development.

## Copyright and License
Copyright 2013 Facjure LLC,  under the Apache 2.0 License.
