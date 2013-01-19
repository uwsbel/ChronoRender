from cr_object import Scriptable

import chronorender.scene as cscene
import chronorender.lighting as clight

class RenderPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderPass(Scriptable):

    @staticmethod
    def getTypeName():
        return "renderpass"

    def __init__(self, *args, **kwargs):
        super(RenderPass,self).__init__(*args, **kwargs)

        self.rndrobjects = []

    def _initMembersDict(self):
        self._members['name']                           = [str, 'nothing']
        self._members['resolution']                     = ['spalist', [640, 480]]
        self._members[cscene.Scene.getTypeName()]       = [cscene.Scene, []]
        self._members[clight.Lighting.getTypeName()]    = [clight.Lighting, []]

    def addRenderable(self, obj):
        if isinstance(obj, list):
            self.rndrobjects += obj
        else:
            self.rndrobjects.append(obj)

    def getOutput(self):
        return "out"

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        for obj in self._rndrobjects:
            obj.render(rib, **kwargs)

def build(**kwargs):
    return RenderPass(**kwargs)
