# Frozen Pie

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery

## Abstract
Have you ever asked someone to show their content on the web?

Reality check: evaluate a CMS, understand templating, filter programming languages, pick a framework, read the docs to customize a workflow, create or tweak existing css, check browser compatibility and mobile-readiness and responsiveness, add plugins for simple logic, and finally, evaluate hosting and pricing options, and so on.

Seriously.

These toolkits are built for developers. For different abstractions. It requires a lot of work for an average user to perform simple tasks, like moving content from one site to another, changing design, modifying templates that are user-friendly, adding simple logic to analyze, filter, and distribute content to apps and devices.

Things shouldn’t be this way. Not in 2013.

## How it works

Frozen Pie is built on _three principles_:

1. Content is King
2. Design once, View anywhere
3. Logic should be declarative, composed of single tasks

Here's a sample workflow:

create_crust
> Content creator creates Posts and Pages in Markdown, with optional YAML meta-data

put_in_pan and add filling
> Designers create generic Templates with HAML and Mustache, and optionally, 3rd-party logic (Mustache lambdas), and package them as 'Recipes'.

add_recipes
> Content creator selects Recipes, modifies templates if needed.

bake_in_oven
> Content creator runs a script to compile everything into a single index.html, _everything_ included

serve
> Content creator runs the script to push index.html onto his/her github :gh-pages

As easy as Pie.

## Technical Overview

Frozen-Pie is built on popular specs that promote simplicity: Markdown, Mustache, HAML, and embraces HTML 5 and CSS3. 
It's written in Python with pure functional programming techniques. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel. Lambdas are used to analyze inline content, realtime, with data stored elsewhere. 

Content authors will learn how to run a script, basics of git, Markdown, and that's okay. 

It's time we give them power.

## Documentation
Under active development.

## Status
Under active development.

## Copyright and License
Copyright 2013 Facjure LLC,  under the Apache 2.0 License.
