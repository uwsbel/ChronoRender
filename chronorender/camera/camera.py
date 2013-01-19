from cr_object import Movable
from cr_scriptable import Scriptable

class Camera(Movable):
    @staticmethod
    def getTypeName():
        return "camera"

    def __init__(self, *args, **kwargs):
        super(Camera,self).__init__(*args, **kwargs)

        self.filename = self.getMember('filename')

    def _initMembersDict(self):
        self._members['filename']   = [str, 'default_camera.rib']

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        return

def build(**kwargs):
    return Scene(**kwargs)
