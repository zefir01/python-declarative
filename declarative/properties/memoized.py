# -*- coding: utf-8 -*-
"""
"""
from .bases import (
    InnerException,
)
from ..abstract.module import Module, ResourceFunction
from ..utilities.unique import (
    NOARG,
    unique_generator
)

_UNIQUE_local = unique_generator()


class AccessError(Exception):
    pass


class ClassMemoizedDescriptor(object):
    """
    Works like a combination of :obj:`property` and :obj:`classmethod` as well as :obj:`~.memoized_property`
    """

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        result = self.fget(cls)
        setattr(cls, self.__name__, result)
        return result


memoized_class_property = ClassMemoizedDescriptor


class MemoizedDescriptor(object):
    """
    wraps a member function just as :obj:`property` but saves its value after evaluation
    (and is thus only evaluated once)
    """
    _declarative_instantiation = True
    _use_prev = False

    def __init__(
            self,
            fget,
            name=None,
            doc=None,
    ):
        self.fget = fget
        if name is None:
            self.__name__ = fget.__name__
        else:
            self.__name__ = name
        if doc is None:
            self.__doc__ = fget.__doc__
        else:
            self.__doc__ = doc

    def __get__(self, obj: Module, cls):
        if obj is None:
            return self
        result = obj.__dict__.get(self.__name__, None)
        if result is None:
            prev = obj.store.get_res()
            if self.__name__ != "child_registry":
                print("Creating " + obj.name + "." + self.__name__)
            try:
                if self.fget.__code__.co_argcount == 2:
                    result = self.fget(obj, prev)
                    obj.child_registry.add(result)
                    result.parent = obj
                    result.name = obj.name + "." + self.__name__
                else:
                    result = self.fget(obj)
                if issubclass(result.__class__, Module):
                    result.init()
            except Exception as e:
                if self.fget.__code__.co_argcount == 2 and prev is not None and self._use_prev:
                    obj.child_registry.add(prev)
                    result = prev
                    print("Error in: {0}.{1}, using previous value".format(obj.name, self.__name__))
                    print(e)
                else:
                    obj.store.error_res("{0}.{1}".format(obj.name, self.__name__))
                    print("Error in: {0}.{1}".format(obj.name, self.__name__))
                    print(e)

            if __debug__:
                if result is NOARG:
                    raise InnerException("Return result was NOARG (usu)")

            # print("SET Value for attr ({0}) in {1}".format(self.__name__, id(obj)))
            obj.__dict__[self.__name__] = result
        return result


def mproperty(
        __func: ResourceFunction,
        **kwargs
):
    def wrap(func):
        desc = MemoizedDescriptor(
            func,
            **kwargs
        )
        return desc

    if __func is not None:
        return wrap(__func)
    else:
        return wrap


def dproperty(
        __func: ResourceFunction,
        **kwargs
):
    return mproperty(
        __func=__func,
        **kwargs
    )
