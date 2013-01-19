from cr_object import Scriptable

import chronorender.scene as cscene
import chronorender.lighting as clight
from chronorender.renderpass import Settings

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

        self.rndrsettings   = self.getMember(Settings.getTypeName())
        self.lighting       = self.getMember(clight.Lighting.getTypeName())
        self.scene          = self.getMember(cscene.Scene.getTypeName())
        self.rndrobjects    = []

    def _initMembersDict(self):
        self._members['name']                           = [str, 'nothing']
        self._members['resolution']                     = ['spalist', [640, 480]]
        self._members[cscene.Scene.getTypeName()]       = [cscene.Scene, []]
        self._members[clight.Lighting.getTypeName()]    = [clight.Lighting, []]
        self._members[Settings.getTypeName()]           = [Settings, []]

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
        for sett in self.rndrsettings:
            sett.render(rib, **kwargs)
        for light in self.lighting:
            light.render(rib, **kwargs)
        for scene in self.scene:
            scene.render(rib, **kwargs)
        for obj in self.rndrobjects:
            obj.render(rib, **kwargs)

def build(**kwargs):
    return RenderPass(**kwargs)
