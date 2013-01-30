# contains all assests needed to start a render job
import glob, re, os

from cr_object import Object
import cr_utils
from chronorender.finder import AssetNotFoundException

from chronorender.renderobject import RenderObject
from chronorender.renderpass import RenderPass
from chronorender.rendersettings import RenderSettings
from chronorender.simulation import Simulation

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():

    def __init__(self, factories, md, *args, **kwargs):
        self.md             = md
        self.settings       = None
        self.rndrpasses     = []
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

    def resolveAssets(self, assetman):
        self.outdir = assetman.getOutPathFor('output')
        try:
            for obj in self.renderables:
                paths = obj.resolveAssets(assetman)
                self.assetpaths.extend(paths)
            for rpass in self.rndrpasses:
                paths = rpass.resolveAssets(assetman)
                self.assetpaths.extend(paths)
        except AssetNotFoundException as err:
            print err

        # get rid of duplicates
        self.assetpaths = list(set(self.assetpaths))
        return self.assetpaths

    def getFrameRange(self):
        maxframes = 0
        for robj in self.renderables:
            if isinstance(robj, Simulation):
                frames = robj.getNumFrames()
                if frames > maxframes:
                    maxframes = frames
        return [0, maxframes-1]
        # return self.settings.framerange

    def getSearchPaths(self):
        return self.settings.searchpaths

    # def getOutputFileDir(self):
        # return cr_utils.getAbsPathRelativeTo(self.settings.out, self.md.filename)

    #def getOutputFilePath(self, framenumber):
        #return out + self.getPaddedFrame(framenumber) + '.'

    def getPaddedFrame(self, framenumber):
        frame = str(framenumber)
        while len(frame) < self.settings.padding:
            frame = '0' + frame
        return frame

    def writeToFile(self, f):
        return

    def render(self, rib, framenum, *args, **kwargs):
        out = []
        #outpath = self.getOutputFilePath(framenum)
        for passnum in range(0, len(self.rndrpasses)):
            rpass = self.rndrpasses[passnum]
            rpass.render(rib, passnum, framenum, 
                    outpath=self.outdir,
                    outpostfix=self.getPaddedFrame(framenum), **kwargs)
            for f in rpass.getOutputs():
                out.append(f)
        return out
