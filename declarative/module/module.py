from typing import Optional

import yaml

from .wraper import Wrapper
from ..abstract.interfaces import Module


class module_property(property):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        super().__init__(fget, fset, fdel, doc)
        self.module_property = True


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

    @property
    def yaml(self):
        l = self._name.split(".")
        short_name = l[len(l) - 1]
        parameters_lst = []
        for attr in self.__class__.__dict__:
            if attr is None:
                continue
            if issubclass(self.__class__.__dict__[attr].__class__, module_property):
                parameters_lst.append(attr)
        y = {
            "apiVersion": "k-processor/v1",
            "kind": "Module",
            "metadata": f"{short_name}-",
            "spec": {
                "parameters": {}
            }
        }
        for p in parameters_lst:
            val = getattr(self, p)
            y["spec"]["parameters"][p] = str(val)
        s = yaml.dump(y)
        return s

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
