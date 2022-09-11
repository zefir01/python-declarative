import io
from typing import Optional

import yaml

from declarative.abstract.interfaces import Store


class Store(Store):
    _single = None

    def __init__(self):
        f = open("test.yaml", "r")
        data = f.read()
        lst = list(yaml.full_load_all(io.StringIO(data)))
        self.list = list(filter(lambda item: item is not None, lst))

    def get_res(self, name: str) -> Optional[str]:
        return ""
        # return None

    @staticmethod
    def get():
        if Store._single is None:
            Store._single = Store()
        return Store._single
