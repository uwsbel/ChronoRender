from cr_movable import Movable
from cr_scriptable import Scriptable

class Scene(Movable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self, *args, **kwargs):
        super(Scene,self).__init__(*args, **kwargs)

        self.filename = self.getMember('filename')
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Scene, self)._initMembersDict()
        self._members['filename']           = [str, 'default.rib']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def resolveAssets(self, assetman):
        out = []
        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        elif self.filename != '':
            out.append(assetman.find(self.filename))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        else:
            rib.RiReadArchive(self.filename)


def build(**kwargs):
    return Scene(**kwargs)
