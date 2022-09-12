import re
from typing import Optional

from declarative.abstract.interfaces import Store
from declarative.yaml.main import parse


class Store(Store):
    _single = None

    def __init__(self):
        f = open("test.yaml", "r")
        data = f.read()
        obj = parse(data, "input")
        self._dict = {}
        if isinstance(obj, list):
            def sort_by_index(obj):
                name = obj.metadata.annotations["k-processor-name"]
                x = re.search('^.+\[(\d)\]$', name)
                index = int(x.group(1))
                return index

            for i in obj:
                try:
                    name = i.metadata.annotations["k-processor-name"]
                    x = re.search('^(.+)\[\d\]$', name)
                    if x is not None:
                        parent_name = x.group(1)
                        if parent_name not in self._dict:
                            self._dict[parent_name] = []
                        self._dict[parent_name].append(i)
                    self._dict[name] = i
                except Exception as e:
                    print("Invalid resource:\n" + str(i))
                    print(e)
            for i in self._dict.keys():
                if isinstance(self._dict[i], list):
                    self._dict[i] = sorted(self._dict[i], key=sort_by_index)
        else:
            try:
                self._dict[obj.metadata.annotations["k-processor-name"]] = obj
            except Exception as e:
                print("Invalid resource:\n" + str(obj))
                print(e)

    def get_res(self, name: str) -> Optional[str]:
        return self._dict.get(name, None)

    @staticmethod
    def get():
        if Store._single is None:
            Store._single = Store()
        return Store._single
