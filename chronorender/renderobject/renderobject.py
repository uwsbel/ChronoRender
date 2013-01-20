# import weakref
from cr_object import Movable
from cr_scriptable import Scriptable
import cr_enums as cre
from itertools import izip

import chronorender.geometry as cg
import chronorender.shader as cs
from cr_types import intlist, floatlist

class RenderObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderObject(Movable):

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
        self.instanced  = self.getMember('instanced')
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(RenderObject, self)._initMembersDict()

        self._members['motionblur']     = [bool, False]
        self._members['instanced']      = [bool, True]
        self._members['multiobject']    = [bool, False]
        self._members['color']          = [floatlist, [1,0,0]]
        self._members['range']          = [intlist, [-1,-1]]
        self._members[cg.Geometry.getTypeName()] = [cg.Geometry, []]
        self._members[cs.Shader.getTypeName()] = [cs.Shader, []]
        self._members['condition']      = [str, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

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
        out = []
        for geo in self.geometry:
            out.extend(geo.resolveAssets(finder))
        for shdr in self.shaders:
            out.extend(shdr.resolveAssets(finder))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        # TODO anythin?
        for geo in self.geometry:
            geo.setAsset(assetname, obj)
        for shdr in self.shaders:
            shdr.setAsset(assetname, obj)

    def render(self, rib, data=[], *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        else:
            for entry in data:
                self._renderSingleObject(rib, record=entry, **kwargs)

    def _renderSingleObject(self, rib, record={}, **kwargs):
        rib.RiAttributeBegin()
        self._renderTransformData(rib, record, **kwargs)
        
        if self.instanced:
            rib.RiObjectInstance(self.getInstanceID())
        else:
            self.renderShape(rib, **kwargs)
        rib.RiAttributeEnd()

    def _renderTransformData(self, rib, record={}):
        pos_x = record[cre.POS_X] if cre.POS_X in record else 0.0
        pos_y = record[cre.POS_Y] if cre.POS_X in record else 0.0
        pos_z = record[cre.POS_Z] if cre.POS_X in record else 0.0
        rib.RiTranslate(pos_x, pos_y, pos_z)

        if cre.EULER_X in record and record[cre.EULER_X] > 0.0:
            rib.RiRotate(record[cre.EULER_X], 1, 0, 0)
        if cre.EULER_Y in record and record[cre.EULER_Y] > 0.0:
            rib.RiRotate(record[cre.EULER_Y], 0, 1, 0)
        if cre.EULER_Z in record and record[cre.EULER_Z] > 0.0:
            rib.RiRotate(record[cre.EULER_Z], 0, 0, 1)

    def renderShape(self, rib, rendershaders=True, **kwargs):
        rib.RiColor(self.color)
        
        if rendershaders:
            for shdr in self.shaders: 
                shdr.render(rib, **kwargs)

        for geo in self.geometry: 
            geo.render(rib, **kwargs)


    def getInstanceables(self):
        return [self]

def build(**kwargs):
    return RenderObject(**kwargs)
