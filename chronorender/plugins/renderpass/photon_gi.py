import os.path 
from chronorender.renderpass.renderpass import RenderPassException
from chronorender.renderpass.photon_pass import PhotonPass
import chronorender.shader as cs

class PhotonGI(PhotonPass):

    @staticmethod
    def getTypeName():
        return "photon_gi"

    def __init__(self, *args, **kwargs):
        super(PhotonGI,self).__init__(*args, **kwargs)

        self.gpm          = None
        if 'factories' in kwargs:
            self.gpm = cs.Shader(name='photon_gi_light.sl', factories=kwargs['factories'])
            self.lighting.append(self.gpm)

    def _initMembersDict(self):
        super(PhotonGI, self)._initMembersDict()

    def resolveAssets(self, assetman):
        # resolve shader
        out = []
        out.extend(self.gpm.resolveAssets(assetman))
        self._resolvedAssetPaths = True
        return out

def build(**kwargs):
    return PhotonGI(**kwargs)
