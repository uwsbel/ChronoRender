# import weakref
from chronorender.cr_movable import Movable
from chronorender.cr_scriptable import Scriptable
import chronorender.cr_enums as cre
from itertools import izip

from chronorender.geometry import Geometry
from chronorender.shader import Shader
from chronorender.cr_types import intlist, floatlist

from chronorender.math import utils
import math
import numpy

class RenderObject(Movable):

    @staticmethod
    def getTypeName():
        return "renderobject"

    def getBaseName(self):
        return RenderObject.getTypeName()

    def __init__(self, *args, **kwargs):
        super(RenderObject,self).__init__(*args, **kwargs)

        self.data         = []
        self.multiobject  = False

        self.geometry   = self.getMember(Geometry.getTypeName())
        self.shaders    = self.getMember(Shader.getTypeName())
        self.condition  = self.getMember('condition')
        self.color      = self.getMember('color')
        self.instanced  = self.getMember('instanced')
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(RenderObject, self)._initMembersDict()

        # self._members['motionblur']     = [bool, False]
        # self._members['range']          = [intlist, [-1,-1]]
        self._members[Geometry.getTypeName()]   = [Geometry, []]
        self._members[Shader.getTypeName()]     = [Shader, []]
        self._members['condition']              = [str, '']
        self._members['color']                  = [floatlist, []]
        self._members['instanced']              = [bool, False]
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def updateMembers(self):
        super(RenderObject, self).updateMembers()

        self.setMember(Geometry.getTypeName(), self.geometry)
        self.setMember(Shader.getTypeName(), self.shaders)
        self.setMember('condition', self.condition)
        self.setMember('instanced', self.instanced)
        self.setMember(Scriptable.getTypeName(), self.script)

    def parseData(self, entry):
        if len(entry) < len(self.data):
            msg = 'invalid data entry for ' + self.name +\
                    '\n  expected: ' + str(self.data) +\
                    '\n  got: ' + str(entry)
            raise Exception(msg)

        ientry = iter(entry)
        idata = iter(self.data)
        return dict(izip(idata, ientry))

    def resolveAssets(self, assetman):
        # TODO anythin?
        out = []
        for geo in self.geometry:
            out.extend(geo.resolveAssets(assetman))
        for shdr in self.shaders:
            out.extend(shdr.resolveAssets(assetman))
        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        # TODO anythin?
        for geo in self.geometry:
            geo.setAsset(assetname, obj)
        for shdr in self.shaders:
            shdr.setAsset(assetname, obj)

    def render(self, rib, data=[], *args, **kwargs):
        if self.script and self.script.isGood():
            rargs = {'data' : data, 'robj' : self}
            rargs = dict(rargs, **kwargs)
            self.script.render(rib, *args, **rargs)
        else:
            # import pdb; pdb.set_trace()
            for entry in data:
                self._renderSingleObject(rib, record=entry, **kwargs)

    def _renderSingleObject(self, rib, record={}, **kwargs):
        rib.AttributeBegin()
        # import pdb; pdb.set_trace()
        self.renderAttributes(rib)
        # import pdb; pdb.set_trace()
        self._renderTransformData(rib, record, **kwargs)
        
        if self.instanced:
            rib.ObjectInstance(self.getInstanceID())
        else:
            self.renderShape(rib, **kwargs)
        rib.AttributeEnd()

    def _renderTransformData(self, rib, record={}, **kwargs):
        pos_x = record[cre.POS_X] if cre.POS_X in record else 0.0
        pos_y = record[cre.POS_Y] if cre.POS_X in record else 0.0
        pos_z = record[cre.POS_Z] if cre.POS_X in record else 0.0

        # Offset for the fact that prman has cone's location
        # at bottom center instead of center.
        if self.geometry[0].getTypeName() == "cone":
            init_vector = numpy.array([[0],[0],[1],[1]])
            rot_matrix = None
            if cre.QUAT_X in record:
                rot_matrix = utils.quaternion_matrix([record[cre.QUAT_W], record[cre.QUAT_X], record[cre.QUAT_Y], record[cre.QUAT_Z]])
            else:
                rot_matrix = utils.euler_matrix([record[cre.EULER_X], record[cre.EULER_Y], record[cre.EULER_Z]])

            rotated = numpy.dot(rot_matrix, init_vector)
            rotated = rotated * -1
            # import pdb; pdb.set_trace()
            rib.Translate(rotated.item(0), rotated.item(1), rotated.item(2))

        rib.Translate(pos_x, pos_y, pos_z)
        if cre.QUAT_X in record:
            ex, ey, ez = utils.euler_from_quaternion([record[cre.QUAT_W], record[cre.QUAT_X], record[cre.QUAT_Y], record[cre.QUAT_Z]], axes='sxyz')
            rib.Rotate(math.degrees(ex), 1, 0, 0)
            rib.Rotate(math.degrees(ey), 0, 1, 0)
            rib.Rotate(math.degrees(ez), 0, 0, 1)


        if cre.EULER_X in record and record[cre.EULER_X] > 0.0:
            rib.Rotate(record[cre.EULER_X], 1, 0, 0)
        if cre.EULER_Y in record and record[cre.EULER_Y] > 0.0:
            rib.Rotate(record[cre.EULER_Y], 0, 1, 0)
        if cre.EULER_Z in record and record[cre.EULER_Z] > 0.0:
            rib.Rotate(record[cre.EULER_Z], 0, 0, 1)

    def renderShape(self, rib, rendershaders=True, colorobject=True, **kwargs):
        if len(self.color) == 3:
            rib.Color(self.color)
        
        if rendershaders:
            for shdr in self.shaders: 
                shdr.render(rib, **kwargs)

        for geo in self.geometry: 
            geo.render(rib, **kwargs)


    def getInstanceables(self):
        return [self]

def build(**kwargs):
    return RenderObject(**kwargs)
