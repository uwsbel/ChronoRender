from cr_object import Scriptable

import chronorender.data as dat

class Simulation(Scriptable):
    @staticmethod
    def getTypeName():
        return "simulation"

    def __init__(self, *args, **kwargs):
        super(Simulation,self).__init__(*args, **kwargs)

        self._data = self.getMember('data')
        self._name = self.getMember('name')

    def _initMembersDict(self):
        self._members['data']   = [dat.DataObject, None]
        self._members['name']   = [str, 'sim']

def build(**kwargs):
    return Simulation(**kwargs)
