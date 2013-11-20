#!/usr/bin/env python
"""
    Functions for loading, manipulating scripts under lambdas as Mustache Lambdas.

    copyright:
        (c) 2013 by Facjure LLC
    license:
        Ecipse Public License; see LICENSE for more details
"""

import os
import imp
import types
from utils import *


def get_module_names(config):
    """Return the module names where lambdas are present"""
    lambdas_path = config['lambdas_path']
    return [f.strip('.py') for f in os.listdir(lambdas_path) if f.endswith('py') and not f.startswith("__")]


@analyze
def load(config, contents_data, dynamic_templates):
    """Load all pure functions from each module under 'lambdas' as a dictionary by funcion name"""
    # recipe should be foo.bar.baz, not .foo.bar.baz or ..foo.bar.baz or foo/bar/baz
    path = config["lambdas_path"] + os.sep
    modules = [imp.load_source(module_name, path + module_name + ".py") for module_name in get_module_names(config)]
    for module in modules:
        module.config = config
        module.contents = contents_data
        module.dynamic_templates = dynamic_templates
    return {name: getattr(mod, name) for mod in modules for name in dir(mod)
            if not name.startswith("__") and type(getattr(mod, name)) == types.FunctionType}
