import weakref
from itertools import izip

class RndrObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrObject(object):
    _RndrObjectPool = weakref.WeakValueDictionary()

    def __new__(cls, name):
        obj = RndrObject._RndrObjectPool.get(name, None)
        if not obj:
            obj = object.__new__(cls)
            RndrObject._RndrObjectPool[name] = obj
            obj.name = name
        return obj

    def __init__(self, name):
        self.idRange = {"begin" : -1, "end" : -1}
        self.bMotionBlur = False
        self.bInstanced = True
        self.bMultiObject = False

        self.name = name
        self.geometry = None
        self.shaders = {}
        self.color = {"r" : 1, "g" : 0, "b" : 0}
        self.data = ['test', 'test2']

    def parseData(self, entry):
        if len(entry) < len(self.data):
            msg = 'invalid data entry for ' + self.name +\
                    '\n  expected: ' + str(self.data) +\
                    '\n  got: ' + str(entry)
            raise RndrObjectException(msg)

        ientry = iter(entry)
        idata = iter(self.data)
        return dict(izip(idata, ientry))

    def render(self, data):
        return str(data)
