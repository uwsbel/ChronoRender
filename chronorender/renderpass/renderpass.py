from cr_renderable import Renderable
from cr_scriptable import Scriptable

import chronorender.scene as cscene
import chronorender.lighting as clight
import settings as csett
import chronorender.camera as ccam

class RenderPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderPass(Renderable):

    @staticmethod
    def getTypeName():
        return "renderpass"

    def __init__(self, *args, **kwargs):
        super(RenderPass,self).__init__(*args, **kwargs)

        self.rndrsettings   = self.getMember(csett.Settings.getTypeName())
        self.lighting       = self.getMember(clight.Lighting.getTypeName())
        self.camera         = self.getMember(ccam.Camera.getTypeName())
        self.scene          = self.getMember(cscene.Scene.getTypeName())
        self.script     = self.getMember(Scriptable.getTypeName())
        self.renderables    = []

    def _initMembersDict(self):
        super(RenderPass, self)._initMembersDict()

        self._members['name']                           = [str, 'nothing']
        self._members[cscene.Scene.getTypeName()]       = [cscene.Scene, []]
        self._members[clight.Lighting.getTypeName()]    = [clight.Lighting, []]
        self._members[ccam.Camera.getTypeName()]        = [ccam.Camera, []]
        self._members[csett.Settings.getTypeName()]     = [csett.Settings, []]
        self._members[Scriptable.getTypeName()] = [Scriptable, None]


    def addRenderable(self, obj):
        if isinstance(obj, list):
            self.renderables.extend(obj)
        elif isinstance(obj, clight.Lighting):
            self.lighting.append(obj)
        elif isinstance(obj, ccam.Camera):
            self.camera.append(obj)
        elif isinstance(obj, cscene.Scene):
            self.scene.append(obj)
        else:
            self.renderables.append(obj)

    def getOutputs(self):
        out = []
        for sett in self.rndrsettings:
            for d in sett.displays:
                out.extend(d.getOutputs())
        return out

    def getName(self):
        return self.rndrsettings.name

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, passnumber, framenumber, outpath, *args, **kwargs):
        super(RenderPass, self).render(rib, **kwargs)
        if self.script:
            self.script.render(rib, *args, **kwargs)
        else:
            rib.RiFrameBegin(passnumber)
            for sett in self.rndrsettings:
                sett.render(rib, outpath, **kwargs)

            self.renderAttributes(rib)

            self._renderInstanceDecls(rib, framenumber=framenumber, **kwargs)

            for cam in self.camera:
                cam.render(rib, **kwargs)

            rib.RiWorldBegin()
            for light in self.lighting:
                light.render(rib, **kwargs)
            for obj in self.renderables:
                obj.render(rib, framenumber=framenumber, **kwargs)
            for scene in self.scene:
                scene.render(rib, **kwargs)
            rib.RiWorldEnd()

            rib.RiFrameEnd()

    def _renderInstanceDecls(self, rib, **kwargs):
        for obj in self.renderables:
            for inst in obj.getInstanceables():
                if not inst.instanced: continue

                rib.RiObjectBegin(__handleid=inst.getInstanceID())
                inst.renderShape(rib, rendershaders=True)
                rib.RiObjectEnd()

def build(**kwargs):
    return RenderPass(**kwargs)
