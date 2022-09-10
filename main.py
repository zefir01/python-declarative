from abc import ABC
from typing import Optional

import declarative
from declarative.module.module import Module
from declarative.module.resource import Resource


class Child(Resource, ABC):
    def __init__(self, id=None):
        self.id = id


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

    @declarative.resource
    #@declarative.resource_pass_errors
    def c2(self, prev: Optional[Resource]) -> Child:
        child = Child(
            id=2,
        )
        raise Exception("Custom error")
        return child


class Root(declarative.Module):
    @declarative.resource
    def m1(self, prev: Optional[Module]):
        #raise Exception("Custom error")
        child = Parent()
        return child


root = Root("Root")
root.init()

print("\nCreated:")
for r in root.get_resources():
    print(r.name)

print("\nErrors:")
for e in root.get_errors():
    print(e.name, e.error)
