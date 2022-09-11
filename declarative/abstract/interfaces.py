from abc import ABC, abstractmethod
from typing import Optional

from declarative.module.overridable_object import OverridableObject


class Store(ABC):
    #@abstractmethod
    @staticmethod
    def get_res(name: str) -> Optional[str]:
        pass

    @staticmethod
    def get():
        pass


class Module(OverridableObject, ABC):
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def parent(self):
        pass


class Wrapper(ABC):

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def error(self):
        pass

    @abstractmethod
    def obj(self):
        pass

    @abstractmethod
    def str(self):
        pass
