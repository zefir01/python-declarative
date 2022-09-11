from declarative.abstract.interfaces import Wrapper, Module
from declarative.properties.utilities import validate_list, UnknownReturnTypeException
from declarative.yaml.main import parse, sanitize


class AccessFailedObjectException(Exception):
    name = None

    def __init__(self, name):
        self.name = name
        super(AccessFailedObjectException, self).__init__("ERROR: Access to failed object: " + name)


class Wrapper(Wrapper):

    @property
    def name(self):
        return self._name

    @property
    def error(self):
        return self._error

    @property
    def obj(self):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._obj

    @property
    def yaml(self):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._yaml

    def _make_yaml(self):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        if isinstance(self._value, str):
            return self._value
        elif issubclass(self._value.__class__, Module):
            return self._value.yaml
        elif isinstance(self._value, list):
            lst = []
            for i in self._value:
                lst.append(i.yaml)
            res = "---\n".join(lst)
            return res
        else:
            raise UnknownReturnTypeException(self._name, self._value.__class__)

    def __init__(self, name, value, parent, error=None):
        self._name = name
        self._error = error
        self._parent = parent

        if issubclass(value.__class__, Module):
            self._value = value
            value.name = name
            value.parent = parent
            value.init()
        elif issubclass(value.__class__, list):
            if len(value) == 0:
                self._value = None
            else:
                validate_list(value, name)
                if issubclass(value[0].__class__, Module):
                    for i in range(len(value)):
                        self._value = value
                        value[i].name = f"{name}[{i}]"
                        value[i].parent = parent
                        value[i].init()
                elif issubclass(value[0].__class__, str):
                    lst = []
                    for i in range(len(value)):
                        v = sanitize(value[i], f"{name}[{i}]")
                        lst.append(v)
                    self._value = "---\n".join(lst)
                else:
                    raise UnknownReturnTypeException(name, value[0].__class__)
        elif value is not None:
            self._value = sanitize(value, name)
            # print(self._value)

        if self._error is not None:
            print("Warning, object failed: " + self._name)
            return
        if self._value is not None and isinstance(self._value, str):
            self._obj = parse(self._value, name)
        self._yaml = self._make_yaml()

    def __call__(self):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._value
