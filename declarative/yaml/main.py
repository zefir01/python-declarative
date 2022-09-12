import io
from contextlib import suppress

import yaml


class Data(dict):
    @property
    def yaml(self):
        return self._yaml

    def __init__(self, dictionary):
        super().__init__()
        self._yaml = yaml.dump(dictionary)
        self.update(dictionary)
        self.__dict__.update(dictionary)
        for a in dictionary.keys():
            value = getattr(self, a)
            if isinstance(value, dict):
                t = type(self.__class__.__name__ + "_" + a, (Data,), {})
                setattr(self, a, t(value))
            elif isinstance(value, list):
                for i in range(len(value)):
                    if issubclass(value[i].__class__, object):
                        t = type(self.__class__.__name__ + "_" + a + str(i), (Data,), {})
                        value[i] = t(value[i])


def _make_object(d, name, index=None):
    _name = name.replace(".", "_")
    if index is None:
        nc = type(_name, (Data,), {})
    else:
        nc = type(_name + str(index), (Data,), {})
    return nc(d)


def parse(res: str, name):
    if res is None or res == "":
        return None
    d = list(yaml.full_load_all(res))
    lst = list(filter(lambda item: item is not None, d))
    if len(lst) == 1:
        obj = _make_object(lst[0], name)
    else:
        obj = []
        for i in range(len(lst)):
            t = _make_object(lst[i], name, i)
            obj.append(t)
    return obj


def sanitize(res: str, name: str):
    l = name.split(".")
    short_name = l[len(l) - 1]
    strings = res.split("\n")
    min = 1000000
    for s in strings:
        count = 0
        for i in range(len(s)):
            if s[i] == " ":
                count += 1
        if count < min:
            min = count
    res = ""
    for s in strings:
        res += s[min:] + "\n"

    lst = list(yaml.full_load_all(io.StringIO(res)))
    lst = list(filter(lambda item: item is not None, lst))
    for i in range(len(lst)):
        item = lst[i]
        if "metadata" not in item:
            item["metadata"] = {}
        with suppress(KeyError):
            del (item["metadata"]["name"])
        with suppress(KeyError):
            del (item["metadata"]["generateName"])
        if len(lst) > 1:
            item["metadata"]["generateName"] = short_name + f"[{i}]-"
        else:
            item["metadata"]["generateName"] = short_name + "-"

        if "annotations" not in item["metadata"]:
            item["metadata"]["annotations"] = {}
        if len(lst) > 1:
            item["metadata"]["annotations"]["k-processor-name"] = name + f"[{i}]"
        else:
            item["metadata"]["annotations"]["k-processor-name"] = name
    y = yaml.dump_all(lst)
    return y
