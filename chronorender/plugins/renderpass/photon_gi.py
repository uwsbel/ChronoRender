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
            # self.gpm = cs.Shader(name='photon_gi_light.sl', factories=kwargs['factories'])
            self.gpm = cs.Shader(name='indirectsurf.sl', factories=kwargs['factories'])
            self.lighting.append(self.gpm)

    def _initMembersDict(self):
        super(PhotonGI, self)._initMembersDict()

    # def render(self, rib, passnumber, framenumber, outpath='', outpostfix='', *args, **kwargs):
        # self._getCurrMapName(framenumber)
        # self.map_attr.setMember('string photonmap', self.map_name)
        # self.gpm.setAsset('photonmap', self.map_name)
        # super(PhotonPass,self).render(rib, passnumber, framenumber, outpath, 
                # outpostfix, *args, **kwargs)

    def resolveAssets(self, assetman):
        # resolve shader
        out = []
        out.extend(self.gpm.resolveAssets(assetman))
        # self.gpm.setAsset('photonmap', self.map_name)
        # params = self.gpm.getParameters()
        # if 'photonmap' not in params:
            # raise RenderPassException('no parameter \'photonmap\' in shader: ' + 
                    # self.gpm.getShaderName())

        self._resolvedAssetPaths = True
        return out

def build(**kwargs):
    return PhotonGI(**kwargs)
