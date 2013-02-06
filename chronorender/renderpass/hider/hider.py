from chronorender.cr_renderable import Renderable

class HiderException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Hider(Renderable):

    @staticmethod
    def getTypeName():
        return "hider"

    def __init__(self, *args, **kwargs):
        super(Hider,self).__init__(*args, **kwargs)
        self._name = name if name != None else self.getMember('name')

    def _initMembersDict(self):
        super(Hider, self)._initMembersDict()

        self._members['name']   = [str, '']

    def render(self, rib, **kwargs):
        rib.Hider(self._name, self._params)

def build(**kwargs):
    return Hider(**kwargs)
