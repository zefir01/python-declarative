from abc import ABC
from typing import Optional

import declarative
from declarative.abstract.module import Module
from declarative.abstract.resource import Resource


class Child(Resource, ABC):
    def __init__(self, id=None):
        self.id = id


class Parent(declarative.Module):

    @declarative.dproperty
    def c1(self, prev: Optional[Resource]):
        child = Child(
            id=1,
        )
        print("made Parent.c1")
        return child

    @declarative.dproperty
    def c2b(self, prev: Optional[Resource]):
        child = Child(
            id=self.c2.id + 0.5
        )
        print("made Parent.c2b")
        return child

    @declarative.dproperty
    def c2(self, prev: Optional[Resource]):
        child = Child(
            id=2,
        )
        raise Exception("Sorry, no numbers below zero")
        print("made Parent.c2")
        return child


class Root(declarative.Module):
    @declarative.dproperty
    def m1(self, prev: Optional[Module]):
        child = Parent()
        print("made Parent1.m1")
        return child


root = Root("Root")
root.init()

print("\nCreated:")
for r in root.get_resources():
    print(r.name)

print("\nErrors:")
for e in root.get_errors():
    print(e)
