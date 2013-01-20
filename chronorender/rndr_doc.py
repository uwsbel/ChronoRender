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
        self.assetfinder    = None
        self.md             = md

        self.renderables    = []
        self.assetpaths     = []
        
        self.initFromMetadata(factories, md)

    def initFromMetadata(self, factories, md):
        self.md = md
        self.settings   = RenderSettings(factories=factories,**md.singleFromType(RenderSettings))

        if not self.settings:
            raise RndrDocException('no ' + RenderSettings.getTypeName() 
                    + ' found in metadata')
        self.assetfinder = Finder(self.settings._searchpaths)

        self._initRenderables(factories, md)
        self._resolveAssets()
        self._addRenderablesToRenderPasses()

    def _initRenderables(self, factories, md):
        for typename, elem in md.getElementsDict().iteritems():
            for e in elem:
                obj = Object(basename=typename, factories=factories, **e)
                if hasattr(obj, 'render'):
                    if isinstance(obj, RenderPass):
                        self.rndrpasses.append(obj)
                    else:
                        self.renderables.append(obj)

    def _resolveAssets(self):
        try:
            for obj in self.renderables:
                self.assetpaths.extend(obj.resolveAssets(self.assetfinder))
        except AssetNotFoundException as err:
            print err

        # get rid of duplicates
        self.assetpaths = list(set(self.assetpaths))

    def _addRenderablesToRenderPasses(self):
        for rpass in self.rndrpasses:
            for robj in self.renderables:
                rpass.addRenderable(robj)

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

    def render(self, rib, *args, **kwargs):
        for i in range(0, len(self.rndrpasses)):
            rpass = self.rndrpasses[i]
            rpass.render(rib, passnumber=i, **kwargs)
