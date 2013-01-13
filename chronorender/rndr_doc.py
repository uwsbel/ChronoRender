# contains all assests needed to start a render job
from rndr_settings import RndrSettings
from cr_object import Object
from rndr_settings import RndrSettings
from rndr_pass import RndrPass
from shader import Shader
from geometry import Geometry

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():

    @staticmethod
    def _singletonFromMD( md, elemtype, bRequired=True):
        elems = md.findAll(elemtype.getTypeName())
        if len(elems) != 1 and bRequired:
            raise RndrDocException('not only ONE ' + elemtype.getTypeName() + ' in metadata')
        return ([elemtype(**inst) for inst in elems])[0]

    @staticmethod
    def _listFromMD(md, elemtype, bRequired=True):
        elems = md.findAll(elemtype.getTypeName())
        if len(elems) <= 0 and bRequired:
            raise RndrDocException('no ' + elemtype.getTypeName() + ' in metadata')
        return [elemtype(**inst) for inst in elems]

    def __init__(self, **kwargs):
        self.settings   = RndrSettings()
        self.rndrpasses = []
        self.shaders    = []
        self.geometry   = []
        self.lighting   = []
        self.scene      = []

    def initFromMetadata(self, md):
        self.settings   = RndrDoc._singletonFromMD(md, RndrSettings)
        self.rndrpasses = RndrDoc._listFromMD(md, RndrPass)
        self.shaders    = RndrDoc._listFromMD(md, Shader)
        self.geometry   = RndrDoc._listFromMD(md, Geometry)
        # TODO lighting and scene

    def resolveAssets(self):
        paths = self.settings.getSearchPaths()

        try:
            for rpass in self.rndrpasses:
                rpass.resolveAssets(paths)
            for shdr in self.shaders:
                shdr.resolveAssets(paths)
            for geo in self.geometry:
                geo.resolveAssets(paths)
        except Exception:
            print 'whoops'
            return
