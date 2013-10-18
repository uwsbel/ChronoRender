from chronorender.cr_movable import Movable
from chronorender.cr_scriptable import Scriptable

# import chronorender.data as dat
# import chronorender.renderobject as cro
from chronorender.data import DataObject
from chronorender.renderobject import RenderObject

class Simulation(Movable):
    @staticmethod
    def getTypeName():
        return "simulation"

    def getBaseName(self):
        return Simulation.getTypeName()

    def __init__(self, *args, **kwargs):
        super(Simulation,self).__init__(*args, **kwargs)

        self._name = self.getMember('name')
        self._data = self.getMember(DataObject.getTypeName())
        self._robjs = self.getMember(RenderObject.getTypeName())
        self.instanced = False
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Simulation, self)._initMembersDict()
        self._members['name']   = [str, 'sim']
        self._members[DataObject.getTypeName()] = [DataObject, None]
        self._members[RenderObject.getTypeName()] = [RenderObject, []]
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def updateMembers(self):
        self.setMember('name', self._name)
        self.setMember(DataObject.getTypeName(), self._data)
        self.setMember(RenderObject.getTypeName(), self._robjs)
        self.setMember(Scriptable.getTypeName(), self.script)

    def getNumFrames(self):
        # return self._data.getNumUniqueElements()
        return self._data.getNumUniqueElements()

    def setData(self, data):
        self._data = data

    def addRenderObject(self, robj):
        self._robjs.append(robj)

    def render(self, ri, framenumber=0, *args, **kwargs):
        if self.script:
            self.script.render(ri, *args, **kwargs)
        else:
            for robj in self._robjs:
                # import pdb; pdb.set_trace()
                data = self._data.getData(framenumber, robj.condition)
                robj.render(ri, data, *args, **kwargs)

    def resolveAssets(self, assetman):
        self._data.resolveAssets(assetman)

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
