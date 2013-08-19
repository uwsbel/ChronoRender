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

        #TODO: numbered fames, compile the shader

        passargs = {'framenumber' : framenumber, 'outpath' : outpath}
        passargs = dict(passargs.items() + kwargs.items())

        rib.FrameBegin(passnumber)
        
        self._renderSettings(rib, **passargs)
        # for sett in self.rndrsettings:
        #     sett.render(rib, outpath, **kwargs)

        self.renderAttributes(rib)

        self._renderInstanceDecls(rib, **passargs)

        self._renderCamera(rib, **passargs) 
        # for cam in self.camera:
        #     cam.render(rib, **kwargs)

        # self._renderLighting(rib, **kwargs)

        rib.WorldBegin()
        
        rib.Attribute("visibility", {"int diffuse": 1})
        rib.Attribute("visibility", {"int specular": 1})
        rib.Attribute("visibility", {"int transmission": 1})
        rib.Attribute("trace", {"float bias": 0.005})
        rib.Attribute("trace", {"int maxdiffusedepth" : self.rndrsettings[0]._params['bounces']})

        # Now we just assume that we use a light shader
        # bRenderShdrs = False if self.occshader.getShaderType() == 'surface' else True
        self._renderLighting(rib, **passargs) 
        # self.occshader.render(rib, **passargs)
        self._renderRenderables(rib, **passargs)
        # for obj in self.renderables:
        #     obj.render(rib, framenumber=framenumber, rendershaders=bRenderShdrs, **kwargs)
        self._renderScene(rib, **passargs)
        # for scene in self.scene:
        #     scene.render(rib, **kwargs)
        rib.WorldEnd()

        rib.FrameEnd()

    def resolveAssets(self, assetman):
        out = self.occshader.resolveAssets(assetman)
        self._resolvedAssetPaths = True
        return out

    def _renderLighting(self, rib, **kwargs):
        # import pdb; pdb.set_trace()
        if self.occshader.getShaderType() == 'light':
            self.occshader.render(rib, **kwargs)
        # else:
        for light in self.lighting:
            light.render(rib, **kwargs)

def build(**kwargs):
    print "build AOPass"
    return AOPass(**kwargs)
