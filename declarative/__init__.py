#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from .properties import (
    resource,
    resource_pass_errors,
)





from .module.module import (
    Module,
)


from .version import (
    version,
    __version__,
)

def first_non_none(*args):
    for a in args:
        if a is not None:
            return a
    return None

FNN = first_non_none

# PropertyAttributeError.__module__ == __name__
