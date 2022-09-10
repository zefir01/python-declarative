from typing import Optional, Callable

import declarative
from declarative.module.module import Module
from declarative.properties.utilities import check_function


class Parent(declarative.Module):

    @declarative.resource
    def c1(self):
        return ""

    @declarative.resource
    def c2b(self, prev: Optional[str]):
        return self.c2() + ""

    #@declarative.resource
    @declarative.resource_pass_errors
    def c2(self, prev: Optional[str]) -> str:
        raise Exception("Custom error")
        return ""


class Root(declarative.Module):
    @declarative.resource
    def m1(self, prev: Optional[str]):
        # raise Exception("Custom error")
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


