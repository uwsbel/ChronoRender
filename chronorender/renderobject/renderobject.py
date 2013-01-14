# import weakref
from cr_object import Scriptable
from itertools import izip

class RenderObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderObject(Scriptable):

    @staticmethod
    def getTypeName():
        return "renderobject"
    # _RndrObjectPool = weakref.WeakValueDictionary()

    # def __new__(cls, name):
        # obj = RndrObject._RndrObjectPool.get(name, None)
        # if not obj:
            # obj = object.__new__(cls)
            # RndrObject._RndrObjectPool[name] = obj
            # obj.name = name
        # return obj

    def __init__(self, *args, **kwargs):
        super(RenderObject,self).__init__(*args, **kwargs)

        self.geometry = None
        self.shaders = {}
        self.data = []

    def _initMembersDict(self):
        self._members['motionblur']   = [bool, False]
        self._members['instanced']    = [bool, True]
        self._members['multiobject']  = [bool, False]
        self._members['color']        = ['spalist', [1,0,0]]
        self._members['range']        = ['spalist', [-1,-1]]
        self._members['geo']          = ['spalist', ['default']]
        self._members['shaders']      = ['spalist', ['default']]

    def parseData(self, entry):
        if len(entry) < len(self.data):
            msg = 'invalid data entry for ' + self.name +\
                    '\n  expected: ' + str(self.data) +\
                    '\n  got: ' + str(entry)
            raise RenderObjectException(msg)

        ientry = iter(entry)
        idata = iter(self.data)
        return dict(izip(idata, ientry))

    def render(self, data):
        return str(data)

def build(**kwargs):
    return RenderObject(**kwargs)