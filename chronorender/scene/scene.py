from cr_object import Movable

class Scene(Movable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self, *args, **kwargs):
        super(Scene,self).__init__(*args, **kwargs)

        self.filename = self.getMember('filename')

    def _initMembersDict(self):
        super(Scene, self)._initMembersDict()
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
