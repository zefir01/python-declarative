from abc import ABC
from typing import Optional

from .overridable_object import OverridableObject
from .wraper import Wrapper


class Store:
    def get_res(self) -> Optional[str]:
        return ""
        # return None


class Module(OverridableObject, ABC):
    name = None
    store = Store()
    parent = None

    def __init__(self, name: Optional[str] = None):
        self.name = name
        super(Module, self).__init__()

    def _get_resources(self) -> set[Wrapper]:
        resources = set()
        for attr in self.__class__.__dict__:
            val = getattr(self, attr)
            if not isinstance(val, Wrapper):
                continue
            resources.add(val)
        return resources

    def get_resources(self) -> set:
        resources = set(filter(lambda r: r.error is None, self._get_resources()))
        for res in resources:
            if issubclass(res().__class__, Module):
                resources = resources.union(res().get_resources())
        if self.parent is None:
            resources.add(Wrapper(self.name, self, None))
        return resources

    def get_errors(self):
        errors = set()
        rr = self._get_resources()
        for r in rr:
            if r.error is not None:
                errors.add(r)
            elif issubclass(r().__class__, Module):
                errors = errors.union(r().get_errors())
        return errors
