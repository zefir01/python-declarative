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

from declarative.abstract.interfaces import Module


def check_function(func: Callable, type: TypeVar):
    cv = type_from_runtime(type)
    res = cv.can_assign(KnownValue(func), CTX)
    if isinstance(res, CanAssignError):
        return False
    return True


class UnknownReturnTypeException(Exception):
    name = None

    def __init__(self, name, type):
        self.name = name
        super(UnknownReturnTypeException, self).__init__(
            f"ERROR: Unknown return type of: {name}, got: {type.__name__}")


def validate_list(lst: list, name: str):
    types_set = set(map(lambda x: x.__class__.__name__, lst))
    if len(types_set) > 1 or (not issubclass(lst[0].__class__, Module) and not isinstance(lst[0], str)):
        raise UnknownReturnTypeException(name, lst[0].__class__)
