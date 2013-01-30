from chronorender.renderpass.renderpass import RenderPassException
from chronorender.renderpass.raytrace_pass import RayTracePass
import chronorender.shader as cs

class EnvLightPass(RayTracePass):

    @staticmethod
    def getTypeName():
        return "envlight"

    def __init__(self, *args, **kwargs):
        super(EnvLightPass,self).__init__(*args, **kwargs)

        self.env = None
        self.envmap = self.getVar('envmap', kwargs)

        if 'factories' in kwargs:
            self.env = cs.Shader(name='envlight.sl', factories=kwargs['factories'])
            self.lighting.append(self.env)

    def _initMembersDict(self):
        super(EnvLightPass, self)._initMembersDict()

        self._members['envmap']   = [str, '']

    def resolveAssets(self, assetman):
        # resolve envmap texture
        if len(self.envmap) <= 0:
            raise RenderPassException('no value given to parameter \'envmap\' for ' + EnvLightPass.getTypeName() + ' pass')

        assetman.find(self.envmap)

        # resolve shader
        out = self.env.resolveAssets(assetman)
        self.env.setAsset('envmap', self.envmap)
        params = self.env.getParameters()
        if 'envmap' not in params:
            raise RenderPassException('no parameter \'envmap\' in shader: ' + self.env.getShaderName())

        self._resolvedAssetPaths = True
        return out

def build(**kwargs):
    return EnvLightPass(**kwargs)
