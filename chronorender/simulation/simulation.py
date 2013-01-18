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

    def _initMembersDict(self):
        self._members[dat.DataObject.getTypeName()] = [dat.DataObject, None]
        self._members['name']   = [str, 'sim']
        self._members[cro.RenderObject.getTypeName()] = [cro.RenderObject, []]

def build(**kwargs):
    return Simulation(**kwargs)
