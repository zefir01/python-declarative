from abc import ABC
from typing import Optional

from .overridable_object import OverridableObject
from ..abstract.module import Module


class Module(OverridableObject, Module, ABC):
    name = None

    def __init__(self, name: Optional[str] = None):
        self.name = name
        super(Module, self).__init__()

    def get_resources(self) -> set:
        resources = set()
        for r in self.child_registry():
            rr = r()
            if issubclass(rr.__class__, OverridableObject):
                resources = resources.union(r.get_resources())
            else:
                resources.add(rr)
        return resources

    def get_errors(self):
        errors = set(self.store.errors)
        for r in self.child_registry():
            if issubclass(r.__class__, Module):
                errors = errors.union(set(r.store.errors))
        return errors
