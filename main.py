from abc import ABC
from typing import Optional

import declarative
from declarative.abstract.module import Module
from declarative.abstract.resource import Resource


class Child(Resource, ABC):
    def __init__(self, id=None):
        self.id = id

def decorator_factory(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return result
        return wrapper
    return decorator

class Parent(declarative.Module):

    @declarative.resource
    def c1(self, prev: Optional[Resource]):
        child = Child(
            id=1,
        )
        return child

    @declarative.resource
    def c2b(self, prev: Optional[Resource]):
        child = Child(
            id=self.c2().id + 0.5
        )
        return child

    @declarative.resource_pass_errors
    def c2(self, prev: Optional[Resource]) -> Child:
        child = Child(
            id=2,
        )
        raise Exception("Custom error")
        return child


class Root(declarative.Module):
    @declarative.resource
    def m1(self, prev: Optional[Module]):
        child = Parent()
        return child


root = Root("Root")
root.init()

print("\nCreated:")
for r in root.get_resources():
    print(r.name)

print("\nErrors:")
for e in root.get_errors():
    print(e)
