# -*- coding: utf-8 -*-
"""
"""
from declarative.module.module import ResourceFunction, Module
from declarative.module.resource import Resource
from declarative.module.wraper import Wrapper


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
            if issubclass(res.__class__, Resource):
                result.parent = obj
                result.name = obj.name + "." + self.__name__
            if issubclass(res.__class__, Module):
                result.init()
            obj.__dict__[self.__name__] = Wrapper(obj.name + "." + self.__name__, res)

        result = obj.__dict__.get(self.__name__, None)
        if result is None:
            prev = obj.store.get_res()
            if self.__name__ != "child_registry":
                print("Creating " + obj.name + "." + self.__name__)
            try:
                if self.__name__ == "child_registry":
                    result = self.fget(obj)
                    obj.__dict__[self.__name__] = Wrapper(obj.name + "." + self.__name__, result)
                elif self.fget.__code__.co_argcount == 2:
                    result = self.fget(obj, prev)
                    register(result)
                else:
                    result = self.fget(obj)
                    register(result)
            except Exception as e:
                if self.__name__ != "child_registry" and prev is not None and self._use_prev:
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
