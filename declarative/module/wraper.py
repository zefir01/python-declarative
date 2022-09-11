from declarative.abstract.interfaces import Wrapper, Module
from declarative.yaml.main import parse


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
        self._value = value
        self._error = error
        self._parent = parent

        if issubclass(value.__class__, Module):
            value.name = name
            value.parent = parent
            value.init()

        if self._error is not None:
            print("Warning, object failed: " + self._name)
            return
        if self._value is not None and isinstance(value, str):
            self._obj = parse(value, name)

    def __call__(self, *args, **kwargs):
        if self._error is not None:
            raise AccessFailedObjectException(self._name)
        return self._value
