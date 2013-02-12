import re

def str2list(string):
    return re.split(r'[\s,|:"]+', string)

class _crlist(object):
    _type = list
    def __new__(cls, vals):
        if isinstance(vals, list):
            return [cls._type(x) for x in vals]
        elif isinstance(vals, dict):
            return [cls._type(x) for x in vals.items()]
        elif isinstance(vals, tuple):
            return map(lambda x: cls._type(x), vals)
        elif isinstance(vals, str):
            lizt = str2list(vals)
            return map(lambda x: cls._type(x), lizt)
        else:
            return [cls._type(vals)]

class floatlist(_crlist):
    _type = float

class intlist(_crlist):
    _type = int

class strlist(_crlist):
    _type = str

class listlist(_crlist):
    _type = list

# TODO Incomplete
class _crlist3(object):
    _type = list
    def __new__(cls, vals):
        if isinstance(vals, list):
            val = 0 if len(vals) < 1 else vals[0]
            while len(vals) < 3:
                vals.append(val)

            return [cls._type(x) for x in vals]
        elif isinstance(vals, dict):
            return [cls._type(x) for x in vals.items()]
        elif isinstance(vals, tuple):
            return map(lambda x: cls._type(x), vals)
        elif isinstance(vals, str):
            lizt = str2list(vals)
            return map(lambda x: cls._type(x), lizt)
        else:
            val = cls._type(vals)
            return [val, val, val]

class floatlist3(_crlist3):
    _type = float
