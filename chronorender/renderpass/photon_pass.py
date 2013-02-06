from renderpass import RenderPassException
from raytrace_pass import RayTracePass
import chronorender.option as option
from chronorender.attribute import Attribute

class PhotonPass(RayTracePass):

    @staticmethod
    def getTypeName():
        return "photon"

    def __init__(self, *args, **kwargs):
        super(PhotonPass,self).__init__(*args, **kwargs)
        self.numphotons   = self.getMember('photons')
        self.map_attr     = None
        self.map_name     = ''

        self._initTransientPhotonMap()

    def _initMembersDict(self):
        super(PhotonPass, self)._initMembersDict()
        self._members['photons']  = [int, 500000]

    def render(self, rib, passnumber, framenumber, outpath='', outpostfix='', *args, **kwargs):
        self._getCurrMapName(framenumber)
        # self.map_attr.setMember('string photonmap', self.map_name)
        self.map_attr.setMember('string globalmap', self.map_name)
        super(PhotonPass,self).render(rib, passnumber, framenumber, outpath, 
                outpostfix, *args, **kwargs)

    def _initTransientPhotonMap(self):
        self._initTransientPhotonMapOptions()
        self._initTransientPhotonMapAttributes()

    def _initTransientPhotonMapOptions(self):
        emit_opt = option.Option(name='photon', **{'int emit' : self.numphotons})
        tran_opt = option.Option(name='photon', **{'string lifetime' : 'transient'})
        opts = [emit_opt, tran_opt]

        for opt in opts:
            self.options.append(opt)

    def _initTransientPhotonMapAttributes(self):
        self.map_attr = Attribute(name='photon', **{'string globalmap' : ''})
        attrs = [self.map_attr]

        for attr in attrs:
            self.attributes.append(attr)

    def _getCurrMapName(self, framenumber):
        self.map_name = self.name + "_" + str(framenumber) + ".gpm"

def build(**kwargs):
    return PhotonPass(**kwargs)
