from cr_object import Scriptable

class Scene(Scriptable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self, *args, **kwargs):
        super(Scene,self).__init__(*args, **kwargs)

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

def build(**kwargs):
    return Scene(**kwargs)
