from cr_movable import Movable
from cr_scriptable import Scriptable

class GeometryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Geometry(Movable):

    @staticmethod
    def getTypeName():
        return "geometry"

    def __init__(self, *args, **kwargs):
        super(Geometry,self).__init__(*args, **kwargs)
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Geometry, self)._initMembersDict()
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def resolveAssets(self, assetman):
        out = []
        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)

def build(**kwargs):
    return Geometry(**kwargs)
