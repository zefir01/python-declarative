from contextlib import suppress

import yaml


class Data(dict):
    def __init__(self, dictionary):
        super().__init__()
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


def parse(res: str, name):
    _name = name.replace(".", "_")
    nc = type(_name, (Data,), {})
    d = yaml.unsafe_load(res)
    sanitize(d, _name)
    obj = nc(d)
    return obj


def sanitize(res: dict, name: str):
    l = name.split("_")
    short_name = l[len(l) - 1]
    with suppress(KeyError):
        del (res["metadata"]["name"])
    with suppress(KeyError):
        del (res["metadata"]["generateName"])
    res["metadata"]["generateName"] = short_name + "-"
    y = yaml.dump(res)
    pass
