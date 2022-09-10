# -*- coding: utf-8 -*-
"""
"""
from __future__ import (
    division,
    print_function,
    absolute_import,
)

from typing import Callable, TypeVar

from pyanalyze.annotations import type_from_runtime
from pyanalyze.test_value import CTX
from pyanalyze.value import KnownValue, CanAssignError


def check_function(func: Callable, type: TypeVar):
    cv = type_from_runtime(type)
    res = cv.can_assign(KnownValue(func), CTX)
    if isinstance(res, CanAssignError):
        return False
    return True
