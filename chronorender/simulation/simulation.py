from cr_movable import Movable
from cr_scriptable import Scriptable

import chronorender.data as dat
import chronorender.renderobject as cro

class Simulation(Movable):
    @staticmethod
    def getTypeName():
        return "simulation"

    def __init__(self, *args, **kwargs):
        super(Simulation,self).__init__(*args, **kwargs)

        self._data = self.getMember(dat.DataObject.getTypeName())
        self._name = self.getMember('name')
        self._robjs = self.getMember(cro.RenderObject.getTypeName())
        self.instanced = False
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Simulation, self)._initMembersDict()
        self._members[dat.DataObject.getTypeName()] = [dat.DataObject, None]
        self._members['name']   = [str, 'sim']
        self._members[cro.RenderObject.getTypeName()] = [cro.RenderObject, []]
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def getNumFrames(self):
        return self._data.getNumUniqueElements()

    def render(self, ri, framenumber=0, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        else:
            for robj in self._robjs:
                data = self._data.getData(framenumber, robj.condition)
                robj.render(ri, data, *args, **kwargs)

    def resolveAssets(self, assetman):

        self._data.resolveSources()

        out = []
        for robj in self._robjs:
            out.extend(robj.resolveAssets(assetman))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        for robj in self._robjs:
            robj.setAsset(assetname, obj)

    def getInstanceables(self):
        out = []
        for robj in self._robjs:
            out.extend(robj.getInstanceables())
        return out

def build(**kwargs):
    return Simulation(**kwargs)
