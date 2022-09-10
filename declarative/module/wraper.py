class AccessFailedObjectException(Exception):
    name = None

    def __init__(self, name):
        self.name = name
        super(AccessFailedObjectException, self).__init__("ERROR: Access to failed object: " + name)


class Wrapper:
    name: str = None
    value = None
    error: Exception = None
    parent = None

    def __init__(self, name, value, parent, error=None):
        self.name = name
        self.value = value
        self.error = error
        self.parent = parent
        if self.error is not None:
            print("Warning, object failed: " + self.name)

    def __call__(self, *args, **kwargs):
        if self.error is not None:
            raise AccessFailedObjectException(self.name)
        return self.value
