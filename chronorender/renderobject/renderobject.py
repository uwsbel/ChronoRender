# import weakref
from cr_object import Scriptable
from itertools import izip

import chronorender.geometry as cg
import chronorender.shader as cs

class RenderObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderObject(Scriptable):

    @staticmethod
    def getTypeName():
        return "renderobject"

    def __init__(self, *args, **kwargs):
        super(RenderObject,self).__init__(*args, **kwargs)

        self.geometry   = self.getMember(cg.Geometry.getTypeName())
        self.shaders    = self.getMember(cs.Shader.getTypeName())
        self.data       = []
        self.condition  = self.getMember('condition')
        self.color      = self.getMember('color')

    def _initMembersDict(self):
        self._members['motionblur']     = [bool, False]
        self._members['instanced']      = [bool, True]
        self._members['multiobject']    = [bool, False]
        self._members['color']          = ['spalist', [1,0,0]]
        self._members['range']          = ['spalist', [-1,-1]]
        self._members[cg.Geometry.getTypeName()] = [cg.Geometry, []]
        self._members[cs.Shader.getTypeName()] = [cs.Shader, []]
        self._members['condition']      = [str, ""]

    def parseData(self, entry):
        if len(entry) < len(self.data):
            msg = 'invalid data entry for ' + self.name +\
                    '\n  expected: ' + str(self.data) +\
                    '\n  got: ' + str(entry)
            raise RenderObjectException(msg)

        ientry = iter(entry)
        idata = iter(self.data)
        return dict(izip(idata, ientry))

    def resolveAssets(self, finder):
        # TODO anythin?
        for geo in self.geometry:
            geo.resolveAssets(finder)
        for shdr in self.shader:
            shdr.resolveAssets(finder)
        self._resolvedAssetPaths = True

    def setAsset(self, assetname, obj):
        # TODO anythin?
        for geo in self.geometry:
            geo.setAsset(assetname, obj)
        for shdr in self.shaders:
            shdr.setAsset(assetname, obj)

    def render(self, data):
        return str(data)

def build(**kwargs):
    return RenderObject(**kwargs)
