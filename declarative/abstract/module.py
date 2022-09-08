from abc import ABCMeta, abstractmethod
from typing import TypeVar, Optional

from declarative.abstract.resource import Resource

T = TypeVar("T")


class Store:
    errors = []

    def get_res(self) -> Optional[Resource]:
        return Resource()
        # return None

    def error_res(self, name: str):
        self.errors.append(name)


class Module(Resource):
    __metaclass__ = ABCMeta
    store = Store()
    parent = None

    @abstractmethod
    def child_registry(self):
        return set()


class ResourceFunction:
    def __call__(self, module: Module, prev: Optional[Resource]) -> Optional[Resource]:
        pass
