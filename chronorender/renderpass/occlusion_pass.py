from chronorender.renderpass.raytrace_pass import RayTracePass
import chronorender.shader as cs

class OcclusionPass(RayTracePass):

    @staticmethod
    def getTypeName():
        return "occlusion"

    def __init__(self, *args, **kwargs):
        super(OcclusionPass,self).__init__(*args, **kwargs)

        self.occ = None
        if 'factories' in kwargs:
            self.occ = cs.Shader(name='occlusionlight.sl', factories=kwargs['factories'])
            self.lighting.append(self.occ)

    def _initMembersDict(self):
        super(OcclusionPass, self)._initMembersDict()

    def resolveAssets(self, assetman):
        out = self.occ.resolveAssets(assetman)
        self._resolvedAssetPaths = True
        return out

def build(**kwargs):
    return OcclusionPass(**kwargs)
