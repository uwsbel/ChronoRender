from cr_object import Scriptable

class Lighting(Scriptable):
    @staticmethod
    def getTypeName():
        return "lighting"

    def __init__(self, *args, **kwargs):
        super(Lighting,self).__init__(*args, **kwargs)

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

def build(**kwargs):
    return Lighting(**kwargs)
