# Frozen Pie

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery

## Abstract
Have you ever asked someone to put their content—text and images, on a custom designed website?

Reality check: evaluate a CMS, understand templating concepts, filter programming languages, pick a framework, read docs on internals to customize a workflow, create or tweak existing css, check browser compatibility and mobile-readiness and responsiveness, add plugins for simple logic, and finally, evaluate hosting and pricing options, and so on.

Seriously.

These toolkits are built for developers. For different abstractions. 

It requires a lot of work for an average, yet smart user to perform simple tasks, like moving content from one site to another, changing design on the fly, modifying templates that are user-friendly, adding basic logic to analyze, filter, and distribute content to any device.

Things shouldn’t be this way. Not in 2013.

## How it works

Frozen Pie is built on _three principles_:

1. Content is King
2. Design once, View anywhere (Responsive Web Design)
3. Logic should be declarative, composed of single tasks (Lambdas)

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

As easy as Frozen Pie.

## Technical Overview

Frozen-Pie is built on popular specs that promote simplicity: Markdown, Mustache, and HAML. It's written in Python (soon, in Clojure) with pure functional programming techniques. There is no state, no framework, just a single workflow that lets content creators, designers, and developers work in parallel. Lambdas are used to analyze content, realtime, with data stored elsewhere. 

Content authors will learn how to run a script, basics of git, Markdown, and that's okay. 

It's time we give them power.

## Documentation
Under active development.

## Status
Under active development.

## Copyright and License
Copyright 2013 Facjure LLC,  under the Apache 2.0 License.
