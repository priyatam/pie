#!/usr/bin/env python
"""
    Utility functions for compiling, transforming CSS, LESS, SCSS.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache License v2.0; see LICENSE for more details.
"""

from scss import Scss
from utils import *


@analyze
def build(config):
    styles_path = config["styles_path"]
    compiler = Scss(scss_opts={"verbosity": True, "compress": False, "load_paths": [styles_path]})
    return unicode(compiler.compile(read("child.scss", styles_path), "utf-8"))
