from typing import Optional

from .wraper import Wrapper
from ..abstract.interfaces import Module


class Module(Module):

    def __init__(self, name: Optional[str] = None):
        self._name = name
        self._parent = None
        super(Module, self).__init__()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    def _get_resources(self):
        resources = set()
        for attr in self.__class__.__dict__:
            val = getattr(self, attr)
            if not issubclass(val.__class__, Wrapper):
                continue
            resources.add(val)
        return resources

    def get_resources(self) -> set:
        resources = set(filter(lambda r: r.error is None, self._get_resources()))
        for res in resources:
            if issubclass(res().__class__, Module):
                resources = resources.union(res().get_resources())
            elif isinstance(res(), list):
                if issubclass(res()[0].__class__, Module):
                    for i in res():
                        resources = resources.union(i.get_resources())
                elif isinstance(res()[0], str):
                    NotImplemented()
                else:
                    raise NotImplemented()
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
