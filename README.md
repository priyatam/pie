# Frozen Pie

> You know you have reached perfection in design, not when there is nothing more to add, but when there is nothing more to be taken away -- Antoine de Saint-Exupery

## Abstract
Have you ever asked your non-programmer friend to create a custom website?

Reality check: evaluate a framework, filter on language, understand its templating syntax, its internals to customize a workflow, modify non-portable css styles, create some, check browser compatibility and responsiveness, evaluate hosting and pricing, avoid plugins that blow on your face, and so on.

These toolkits are built for developers. For different abstractions. It requires a lot of work for an average, yet smart user to perform simple tasks, like changing content and design on the fly, adding simple logic to analyze data, build, and filter content from any device.

Things shouldn’t be this way.

## How it works

Frozen is built on three principles:

1. Content is King
2. Design once, View anywhere (Responsive Web Design)
3. Logic should be composed of simple, declarative tasks (lambdas)

Here's a sample workflow:

create_crust
> Content creator creates Posts and Pages in Markdown, with optional YAML meta-data

put_in_pan and add filling
> Designers create generic Templates with HAML and Mustache, and optionally, 3rd party logic (Mustache lambdas). Then, they package them as 'Recipes'.

add_recipes
> Content creator selects Recipes, modifies templates if needed.

bake_in_oven
> Content creator runs a script to compile everything into a single index.html, _everything_ included

serve
> Content creator runs the script to push index.html onto his/her github :gh-pages

As easy as Frozen Pie.

## Technical Overview

Frozen-Pie is built in Python (soon, in Clojure) with pure functional programming techniques. There is no state, no framework, just a simple workflow that lets content creators, designers, and developers work in parallel.

It builds on popular specs that promote simplicity: Markdown, Mustache, and HAML.

## Documentation
Under active development.

## Status
Under active development.

## Copyright and License
Copyright 2013 Facjure LLC,  under the Apache 2.0 License.
