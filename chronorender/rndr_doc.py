# contains all assests needed to start a render job
from cr_object import Object
from rendersettings import RenderSettings
from renderpass import RenderPass
from shader import Shader
from geometry import Geometry

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():

    def _constructObject(self, instance, elemtype):
        qual = elemtype.getInstanceQualifier()
        if qual not in instance:
            instance[qual] = elemtype.getTypeName()
        concr_name = instance[qual]
        return self.factories[elemtype.getTypeName()].build(concr_name, **instance)

    def _singletonFromMD(self, elemtype, bRequired=True):
        elems = self.md.findAll(elemtype.getTypeName())
        if len(elems) != 1 and bRequired:
            raise RndrDocException('not only ONE ' + elemtype.getTypeName() + ' in metadata')
        return self._constructObject(elems[0], elemtype)

    def _listFromMD(self, elemtype, bRequired=True):
        elems = self.md.findAll(elemtype.getTypeName())
        if len(elems) <= 0 and bRequired:
            raise RndrDocException('no ' + elemtype.getTypeName() + ' in metadata')

        out = []
        for inst in elems:
            out.append(self._constructObject(inst, elemtype))
        return out


    def __init__(self, factories, md=None, **kwargs):
        self.settings   = RenderSettings()
        self.rndrpasses = []
        self.shaders    = []
        self.geometry   = []
        self.lighting   = []
        self.scene      = []
        self.factories  = factories
        
        if md != None:
            self.initFromMetadata(md)

    def initFromMetadata(self, md):
        self.md = md
        self.settings   = self._singletonFromMD(RenderSettings)
        self.rndrpasses = self._listFromMD(RenderPass)
        self.shaders    = self._listFromMD(Shader)
        self.geometry   = self._listFromMD(Geometry)
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
