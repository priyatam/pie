#!/usr/bin/env python
"""
    Utility functions for compiling, transforming CSS, LESS, SCSS.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Apache 2.0 License; see LICENSE for more details.
"""

import scss
import cssmin
from utils import *


@analyze
def compile(config):
    styles_path = config["styles_path"]
    compiler = scss.Scss(scss_opts={"verbosity": True, "compress": False, "load_paths": [styles_path]})
    return unicode(compiler.compile(read("style.scss", styles_path), "utf-8"))
