# contains all assests needed to start a render job
import glob, re, os

from cr_object import Object
import cr_utils
from chronorender.finder import AssetNotFoundException

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
        self.md             = md

        self.renderables    = []
        self.assetpaths     = []
        self.outdir         = ""
        
        self.initFromMetadata(factories, md)

    def __str__(self):
        out = str(self.settings)
        for rpass in self.rndrpasses:
            out += str(rpass)
        for rndr in self.renderables:
            out += str(rndr)
        return out

    def initFromMetadata(self, factories, md):
        self.md = md
        self.settings   = RenderSettings(factories=factories,**md.singleFromType(RenderSettings))

        if not self.settings:
            raise RndrDocException('no ' + RenderSettings.getTypeName() 
                    + ' found in metadata')

        self._initRenderables(factories, md)
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

    def _addRenderablesToRenderPasses(self):
        for rpass in self.rndrpasses:
            for robj in self.renderables:
                rpass.addRenderable(robj)

    def resolveAssets(self, finder):
        try:
            for obj in self.renderables:
                self.assetpaths.extend(obj.resolveAssets(finder))
        except AssetNotFoundException as err:
            print err

        # get rid of duplicates
        self.assetpaths = list(set(self.assetpaths))
        return self.assetpaths

    def getFrameRange(self):
        return self.settings.framerange

    def getSearchPaths(self):
        return self.settings.searchpaths

    # def getOutputFileDir(self):
        # return cr_utils.getAbsPathRelativeTo(self.settings.out, self.md.filename)

    def getOutputFilePath(self, framenumber):
        frame = str(framenumber)
        while len(frame) < self.settings.padding:
            frame = '0' + frame
        out = os.path.join(self.outdir, 'out.')
        return out + frame + '.'

    def writeToFile(self, f):
        return

    def render(self, rib, framenumber, *args, **kwargs):
        out = []
        outpath = self.getOutputFilePath(framenumber)
        for i in range(0, len(self.rndrpasses)):
            rpass = self.rndrpasses[i]
            rpass.render(rib, i, framenumber, outpath, **kwargs)
            for f in rpass.getOutputs():
                out.append(outpath+f)
        return out
