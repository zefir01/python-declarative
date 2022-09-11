from declarative.abstract.interfaces import Wrapper, Module
from declarative.yaml.main import parse, sanitize


class AccessFailedObjectException(Exception):
    name = None

    def __init__(self, name):
        self.name = name
        super(AccessFailedObjectException, self).__init__("ERROR: Access to failed object: " + name)


class Wrapper(Wrapper):
    _name: str = None
    _value = None
    _error: Exception = None
    _parent = None
    _obj = None

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
    def str(self):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._value

    def __init__(self, name, value, parent, error=None):
        self._name = name
        self._error = error
        self._parent = parent

        if issubclass(value.__class__, Module):
            self._value = value
            value.name = name
            value.parent = parent
            value.init()
        elif value is not None:
            self._value = sanitize(value, name)
            #print(self._value)

        if self._error is not None:
            print("Warning, object failed: " + self._name)
            return
        if self._value is not None and isinstance(self._value, str):
            self._obj = parse(self._value, name)

    def __call__(self, *args, **kwargs):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._value
