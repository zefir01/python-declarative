#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from .properties import (
    HasDeclaritiveAttributes,
    resource,
    resource_pass_errors,
    PropertyTransforming,
    PropertyAttributeError,
    group_dproperty,
    group_mproperty,
    mproperty_adv,
    dproperty_adv,
    mproperty_adv_group,
    dproperty_adv_group,
)





from .module.module import (
    Module,
)

from .metaclass import (
    AutodecorateMeta,
    Autodecorate,
    AttrExpandingObject,
    GetSetAttrExpandingObject,
)

from .utilities.unique import (
    NOARG,
    unique_generator,
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

PropertyAttributeError.__module__ == __name__
