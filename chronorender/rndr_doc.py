# contains all assests needed to start a render job
import glob, re, os

from cr_object import Object
from finder import Finder, AssetNotFoundException

from chronorender.renderobject import RenderObject
from chronorender.renderpass import RenderPass
from chronorender.rendersettings import RenderSettings
from chronorender.shader import Shader
from chronorender.geometry import Geometry

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():

    def __init__(self, factories, md, *args, **kwargs):
        self.settings       = None
        self.rndrobjs       = []
        self.rndrpasses     = []
        self.shaders        = []
        self.geometry       = []
        self.lighting       = []
        self.scene          = []
        self.factories      = factories
        self.assetfinder    = None
        self.md             = md
        
        self.initFromMetadata(md)

    def initFromMetadata(self, md):
        self.md = md
        self.settings   = self.factories.buildObject(RenderSettings, md.singleFromType(RenderSettings))
        self.rndrobjs   = self.factories.buildObject(RenderObject, md.listFromType(RenderObject))
        self.rndrpasses = self.factories.buildObject(RenderPass, md.listFromType(RenderPass))
        self.shaders    = self.factories.buildObject(Shader, md.listFromType(Shader))
        self.geometry   = self.factories.buildObject(Geometry, md.listFromType(Geometry))
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
