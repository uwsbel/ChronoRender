from chronorender.cr_renderable import Renderable
from chronorender.cr_scriptable import Scriptable

import hider as hider
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

        self.name           = self.getMember('name')
        self.rndrsettings   = self.getMember(csett.Settings.getTypeName())
        self.lighting       = self.getMember(clight.Lighting.getTypeName())
        self.camera         = self.getMember(ccam.Camera.getTypeName())
        self.scene          = self.getMember(cscene.Scene.getTypeName())
        self.script         = self.getMember(Scriptable.getTypeName())
        self.hiders         = self.getMember(hider.Hider.getTypeName())
        self.renderables    = []

    def _initMembersDict(self):
        super(RenderPass, self)._initMembersDict()

        self._members['name']                           = [str, 'pass']
        self._members[cscene.Scene.getTypeName()]       = [cscene.Scene, []]
        self._members[clight.Lighting.getTypeName()]    = [clight.Lighting, []]
        self._members[ccam.Camera.getTypeName()]        = [ccam.Camera, []]
        self._members[csett.Settings.getTypeName()]     = [csett.Settings, []]
        self._members[Scriptable.getTypeName()]         = [Scriptable, None]
        self._members[hider.Hider.getTypeName()]        = [hider.Hider, []]          

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

    def resolveAssets(self, assetman):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, passnumber, framenumber, 
            outpath='', outpostfix='', *args, **kwargs):
        passargs = {'framenumber' : framenumber, 'outpath' : outpath, 'outpostfix' : outpostfix}
        passargs = dict(passargs.items() + kwargs.items())

        if self.script:
            self.script.render(rib, *args, **passargs)
        else:
            rib.FrameBegin(passnumber)
            self._renderSettings(rib, **passargs)

            self.renderOptions(rib)
            self.renderAttributes(rib)

            self._renderInstanceDecls(rib, **passargs)

            self._renderCamera(rib, **passargs)

            self._renderHider(rib, **passargs)

            rib.WorldBegin()
            self._renderLighting(rib, **passargs)
            self._renderRenderables(rib, **passargs)
            self._renderScene(rib, **passargs)
            rib.WorldEnd()

            rib.FrameEnd()

    def _renderSettings(self, rib, outpath, outpostfix, **kwargs):
        for sett in self.rndrsettings:
            sett.render(rib, outpath, outpostfix, **kwargs)

    def _renderInstanceDecls(self, rib, **kwargs):
        for obj in self.renderables:
            for inst in obj.getInstanceables():
                if not inst.instanced: continue

                rib.ObjectBegin(__handleid=inst.getInstanceID())
                inst.renderShape(rib, rendershaders=True)
                rib.ObjectEnd()

    def _renderCamera(self, rib, **kwargs):
        for cam in self.camera:
            cam.render(rib, **kwargs)

    def _renderHider(self, rib, **kwargs):
        for hider in self.hiders:
            hider.render(rib, **kwargs)

    def _renderLighting(self, rib, **kwargs):
        for light in self.lighting:
            light.render(rib, **kwargs)

    def _renderRenderables(self, rib, **kwargs):
        for obj in self.renderables:
            # obj.render(rib, framenumber=framenumber, **kwargs)
            obj.render(rib, **kwargs)

    def _renderScene(self, rib, **kwargs):
        for scene in self.scene:
            scene.render(rib, **kwargs)

def build(**kwargs):
    return RenderPass(**kwargs)
