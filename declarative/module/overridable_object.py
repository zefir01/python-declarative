# -*- coding: utf-8 -*-
"""
"""
import types
from abc import ABCMeta, abstractmethod

from .bases import HasDeclaritiveAttributes
from ..utilities import SuperBase


class OverridableObject(HasDeclaritiveAttributes, SuperBase, object):
    __metaclass__ = ABCMeta
    """
    """
    _overridable_object_save_kwargs = False
    _overridable_object_kwargs = None
    _initialized = False

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def parent(self):
        pass

    def _overridable_object_inject(self, **kwargs):
        """
        """
        kwargs_unmatched = {}
        for key, obj in list(kwargs.items()):
            try:
                parent_desc = getattr(self.__class__, key)
            except AttributeError:
                kwargs_unmatched[key] = obj
                continue

            if isinstance(
                    parent_desc, (
                            types.MethodType,
                            staticmethod,
                            classmethod
                    )
            ):
                raise ValueError(
                    (
                        "Can only redefine non-method descriptors, {0} a method of class {1}"
                    ).format(key, self.__class__.__name__)
                )
            try:
                use_bd = parent_desc._force_boot_dict
            except AttributeError:
                use_bd = False

            if not use_bd:
                setattr(self, key, obj)
            else:
                self.__boot_dict__[key] = obj
        return kwargs_unmatched

    def __init__(self, **kwargs):
        """
        """
        if self._overridable_object_save_kwargs:
            self._overridable_object_kwargs = kwargs
        kwargs_unmatched = self._overridable_object_inject(**kwargs)
        if kwargs_unmatched:
            raise ValueError(
                (
                    "Can only redefine class-specified attributes, class {0} does not have elements {1}"
                ).format(self.__class__.__name__, list(kwargs_unmatched.keys()))
            )

        # super(OverridableObject, self).__init__()
        return

    def init(self):
        if self._initialized:
            return
        self._initialized = True
        if self.parent is None:
            print("Creating", self.name)
        super(OverridableObject, self).__init__()
