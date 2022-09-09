from abc import ABCMeta, abstractmethod


class Resource:
    __metaclass__ = ABCMeta
    name = None
    id = 0
    parent = None

    @abstractmethod
    def restore(self, json: str):
        pass

    def __call__(self):
        return self
