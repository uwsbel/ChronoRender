# contains all assests needed to start a render job
import glob, re, os

from cr_object import Object
from finder import Finder, AssetNotFoundException

from renderobject import RenderObject
from renderpass import RenderPass
from rendersettings import RenderSettings
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
        self.settings       = RenderSettings()
        self.rndrobjs       = []
        self.rndrpasses     = []
        self.shaders        = []
        self.geometry       = []
        self.lighting       = []
        self.scene          = []
        self.factories      = factories
        self.assetfinder    = None
        
        if md != None:
            self.initFromMetadata(md)

    def initFromMetadata(self, md):
        self.md = md
        self.settings   = self._singletonFromMD(RenderSettings)
        self.rndrobjs   = self._listFromMD(RenderObject)
        self.rndrpasses = self._listFromMD(RenderPass)
        self.shaders    = self._listFromMD(Shader)
        self.geometry   = self._listFromMD(Geometry)
        self.assetfinder = Finder(self.settings._searchpaths)
        # TODO lighting and scene
        self._resolveAssets()

    def _resolveAssets(self):
        try:
            for rpass in self.rndrpasses:
                rpass.resolveAssets(self.assetfinder)
            for shdr in self.shaders:
                shdr.resolveAssets(self.assetfinder)
            for geo in self.geometry:
                geo.resolveAssets(self.assetfinder)
        except AssetNotFoundException as err:
            print err

    def getFrameRange(self):
        return [int(x) for x in self.settings._framerange]

    def getInputDataFiles(self):
        return glob.glob(self.settings._in)

    def getOutputFileDir(self):
        return os.path.abspath(os.path.split(self.settings._out)[0])

    def getOutputDataFilePath(self, framenumber):
        padd = self.settings._padding

        frame = str(framenumber)
        while len(frame) < padd:
            frame = '0' + frame
        outfile = self.settings._out
        return re.sub('#+', frame, outfile)

    def getOutputFileNameForFrameNumber(self, frame):
        return '' 

    def makeDocRelative(self):
        return

    def writeToFile(self, f):
        return

    def render(self, rib, **kwargs):
        for geo in self.geometry:
            geo.render(rib, **kwargs)
        return
