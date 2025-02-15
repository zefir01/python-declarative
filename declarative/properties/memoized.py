# -*- coding: utf-8 -*-
"""
"""
from typing import Callable, Any

from declarative.abstract.interfaces import MemoizedDescriptor
from declarative.module.module import Module
from declarative.module.store import Store
from declarative.module.wraper import Wrapper
from declarative.properties.utilities import check_function


class UnknownMethodSignatureException(Exception):
    name = None

    def __init__(self, name):
        self.name = name
        super(UnknownMethodSignatureException, self).__init__("ERROR: Unknown method signature: " + name)


class MemoizedDescriptor(MemoizedDescriptor):
    """
    wraps a member function just as :obj:`property` but saves its value after evaluation
    (and is thus only evaluated once)
    """
    _declarative_instantiation = True
    _use_prev = False

    def __init__(
            self,
            fget,
            use_prev=False
    ):
        self.fget = fget
        self.__name__ = fget.__name__
        self._use_prev = use_prev

    def __get__(self, obj: Module, cls):
        if obj is None:
            return self

        result = obj.__dict__.get(self.__name__, None)
        if result is None:
            name = obj.name + "." + self.__name__
            print("Creating", name)
            prev = Store.get().get_res(name)
            if check_function(self.fget, Callable[[Module, Any], Any]):
                pass_prev = True
            elif check_function(self.fget, Callable[[Module], Any]):
                pass_prev = False
            else:
                raise UnknownMethodSignatureException(name)
            try:
                if pass_prev:
                    result = self.fget(obj, prev)
                else:
                    result = self.fget(obj)
                result = Wrapper(name, result, obj)
                obj.__dict__[self.__name__] = result
            except Exception as e:
                if prev is not None and self._use_prev:
                    result = Wrapper(name, prev, obj)
                    obj.__dict__[self.__name__] = result
                    print("Exception: ", name, e)
                    print("Warning: {0} failed, using previous value".format(name))
                else:
                    # print("Error in: {0}.{1}".format(obj.name, self.__name__))
                    print("Exception: ", name, e)
                    result = Wrapper(name, None, obj, e)
                    obj.__dict__[self.__name__] = result

        return result


def resource(
        __func,
        **kwargs
):
    def wrap(func):
        desc = MemoizedDescriptor(
            func
        )
        return desc

    return wrap(__func)


def resource_pass_errors(
        __func,
        **kwargs
):
    def wrap(func):
        desc = MemoizedDescriptor(
            func,
            use_prev=True
        )
        return desc

    return wrap(__func)
