from cr_object import Scriptable

class Scene(Scriptable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self, *args, **kwargs):
        super(Scene,self).__init__(*args, **kwargs)

        self.filename = self.getMember('filename')

    def _initMembersDict(self):
        self._members['filename']           = [str, 'default.rib']

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        return


def build(**kwargs):
    return Scene(**kwargs)
