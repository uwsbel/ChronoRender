from cr_object import Movable
from cr_scriptable import Scriptable

class Camera(Movable):
    @staticmethod
    def getTypeName():
        return "camera"

    def __init__(self, *args, **kwargs):
        super(Camera,self).__init__(*args, **kwargs)

        self.filename   = self.getMember('filename')
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Camera, self)._initMembersDict()
        self._members['filename']   = [str, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def resolveAssets(self, finder):
        out = []
        if self.script:
            out.extend(self.script.resolveAssets(finder))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        elif self.filename != '':
            rib.RiReadArchive(self.filename)
        else:
            print "NO SCRIPT"

def build(**kwargs):
    return Camera(**kwargs)
