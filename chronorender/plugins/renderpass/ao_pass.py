from chronorender.renderpass import RenderPass
import chronorender.shader as cs

class RenderPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class AOPass(RenderPass):

    @staticmethod
    def getTypeName():
        return "ao"

    def __init__(self, *args, **kwargs):
        super(AOPass,self).__init__(*args, **kwargs)

        self.occshader = self.getMember(cs.Shader.getTypeName())

    def _initMembersDict(self):
        super(AOPass, self)._initMembersDict()

        self._members[cs.Shader.getTypeName()] = [cs.Shader, None]

    def render(self, rib, passnumber, framenumber, outpath, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # super(AOPass, self).render(rib, passnumber, framenumber, 
                                    # outpath, *args, **kwargs)


        rib.FrameBegin(passnumber)
        for sett in self.rndrsettings:
            sett.render(rib, outpath, **kwargs)

        self.renderAttributes(rib)

        self._renderInstanceDecls(rib, framenumber=framenumber, **kwargs)

        for cam in self.camera:
            cam.render(rib, **kwargs)

        self._renderLighting(rib, **kwargs)

        rib.WorldBegin()
        bRenderShdrs = False if self.occshader.getShaderType() == 'surface' else True
        self.occshader.render(rib, **kwargs)
        for obj in self.renderables:
            obj.render(rib, framenumber=framenumber, rendershaders=bRenderShdrs, **kwargs)
        for scene in self.scene:
            scene.render(rib, **kwargs)
        rib.WorldEnd()

        rib.FrameEnd()

    def resolveAssets(self, assetman):
        out = self.occshader.resolveAssets(assetman)
        self._resolvedAssetPaths = True
        return out

    def _renderLighting(self, rib, **kwargs):
        if self.occshader.getShaderType() == 'light':
            self.occshader.render(rib, **kwargs)
        else:
            for light in self.lighting:
                light.render(rib, **kwargs)

def build(**kwargs):
    print "build AOPass"
    return AOPass(**kwargs)
