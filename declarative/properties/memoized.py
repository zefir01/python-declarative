# -*- coding: utf-8 -*-
"""
"""
from typing import Callable, Optional, Any

from declarative.module.module import ResourceFunction, Module
from declarative.module.wraper import Wrapper
from declarative.properties.utilities import check_function


class UnknownMethodSignatureException(Exception):
    name = None

    def __init__(self, name):
        self.name = name
        super(UnknownMethodSignatureException, self).__init__("ERROR: Unknown method signature: " + name)


class MemoizedDescriptor(object):
    """
    wraps a member function just as :obj:`property` but saves its value after evaluation
    (and is thus only evaluated once)
    """
    _declarative_instantiation = True
    _use_prev = False

    def __init__(
            self,
            fget: ResourceFunction,
            use_prev=False
    ):
        self.fget = fget
        self.__name__ = fget.__name__
        self._use_prev = use_prev

    def __get__(self, obj: Module, cls):
        if obj is None:
            return self

        def register(res):
            if issubclass(res.__class__, Module):
                result.name = obj.name + "." + self.__name__
                result.parent = obj
                result.init()
            obj.__dict__[self.__name__] = Wrapper(obj.name + "." + self.__name__, res)

        result = obj.__dict__.get(self.__name__, None)
        if result is None:
            print("Creating " + obj.name + "." + self.__name__)
            prev = obj.store.get_res()
            if check_function(self.fget, Callable[[Module], Any]):
                pass_prev = False
            elif check_function(self.fget, Callable[[Module, str], Any]) \
                    or check_function(self.fget, Callable[[Module, Optional[str]], Any]):
                pass_prev = True
            elif check_function(self.fget, Callable[[Module], Module]):
                pass_prev = False
            elif check_function(self.fget, Callable[[Module, str], Any]) \
                    or check_function(self.fget, Callable[[Module, Optional[str]], Any]):
                pass_prev = True
            else:
                raise UnknownMethodSignatureException(obj.name + "." + self.__name__)
            try:
                if pass_prev:
                    result = self.fget(obj, prev)
                else:
                    result = self.fget(obj)
                register(result)
            except Exception as e:
                if prev is not None and self._use_prev:
                    result = prev
                    register(result)
                    print(e)
                    print("Error in: {0}.{1}, using previous value".format(obj.name, self.__name__))
                else:
                    # print("Error in: {0}.{1}".format(obj.name, self.__name__))
                    print(e)
                    obj.__dict__[self.__name__] = Wrapper(obj.name + "." + self.__name__, result, e)
                    return None

        return result


def resource(
        __func: ResourceFunction,
        **kwargs
):
    def wrap(func: ResourceFunction):
        desc = MemoizedDescriptor(
            func
        )
        return desc

    return wrap(__func)


def resource_pass_errors(
        __func: ResourceFunction,
        **kwargs
):
    def wrap(func: ResourceFunction):
        desc = MemoizedDescriptor(
            func,
            use_prev=True
        )
        return desc

    return wrap(__func)
