from cr_object import Movable
from cr_scriptable import Scriptable

class Lighting(Movable):
    @staticmethod
    def getTypeName():
        return "lighting"

    def __init__(self, *args, **kwargs):
        super(Lighting,self).__init__(*args, **kwargs)
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Lighting, self)._initMembersDict()
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)

def build(**kwargs):
    return Lighting(**kwargs)
