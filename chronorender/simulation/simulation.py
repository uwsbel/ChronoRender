from cr_object import Scriptable

import chronorender.data as dat
import chronorender.renderobject as cro

class Simulation(Scriptable):
    @staticmethod
    def getTypeName():
        return "simulation"

    def __init__(self, *args, **kwargs):
        super(Simulation,self).__init__(*args, **kwargs)

        self._data = self.getMember(dat.DataObject.getTypeName())
        self._name = self.getMember('name')
        self._robjs = self.getMember(cro.RenderObject.getTypeName())
        self.instanced = False

    def _initMembersDict(self):
        self._members[dat.DataObject.getTypeName()] = [dat.DataObject, None]
        self._members['name']   = [str, 'sim']
        self._members[cro.RenderObject.getTypeName()] = [cro.RenderObject, []]

    def render(self, ri, framenumber=0, *args, **kwargs):
        for robj in self._robjs:
            data = self._data.getData(framenumber, robj.condition)
            robj.render(ri, data, *args, **kwargs)

    def resolveAssets(self, finder):
        out = []
        for robj in self._robjs:
            out.extend(robj.resolveAssets(finder))
        self._resolvedAssetPaths = True
        return out

    def getInstanceables(self):
        out = []
        for robj in self._robjs:
            out.extend(robj.getInstanceables())
        return out

def build(**kwargs):
    return Simulation(**kwargs)
