import datetime, os, logging, glob

import chronorender.cr_utils as crutils
import chronorender.metadata as md
import chronorender.rndr_doc as rd
import chronorender.ri as ri
from chronorender.rndr_job_assetmanager import RndrJobAssetManager

class RndrJobException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrJob():
    def __init__(self, infile, factories):
        self.stream         = None
        self._metadata      = md.MetaData(infile)
        self._rndrdoc       = rd.RndrDoc(factories, self._metadata)
        self._rootdir       = os.path.abspath(os.path.split(self._metadata.filename)[0])
        self._timecreated   = datetime.datetime.now()
        self._renderer      = None
        self._frames        = None
        self._assetman      = RndrJobAssetManager(self._rootdir, self._rndrdoc)

    def run(self, framerange=None):
        self._assetman.createOutDirs()
        prevdir = os.getcwd()
        try:
            os.chdir(self._rootdir)
            self._resolveAssets(framerange)
            self._render()
        except Exception as err:
            raise err
        finally:
            os.chdir(prevdir)

    def _resolveAssets(self, framerange=None):
        self._assetman.updateAssets()
        self._assetman.compileShaders(self.stream)
        self._verifyFrameRange(framerange)

    def _render(self):
        self._startRenderer(ri.rmanlibutil.libFromRenderer(self.stream))
        self._renderOptions()
        self._renderFrames()
        self._stopRenderer()

    def _renderOptions(self):
        cr_paths = crutils.getCRAssetPaths()
        cr_pathsstr = reduce(lambda x, y: str(x) + ":" + str(y), cr_paths)
        cr_pathsstr += ":"
        self._renderer.RiOption("searchpath", "shader",
                cr_pathsstr + self._assetman.getOutPathFor("shader") + ":@")
        self._renderer.RiOption("searchpath", "procedural",
                cr_pathsstr + self._assetman.getOutPathFor("script") + ":@")
        self._renderer.RiOption("searchpath", "texture",
                cr_pathsstr + self._assetman.getOutPathFor("texture") + ":@")
        self._renderer.RiOption("searchpath", "archive",
                cr_pathsstr + self._assetman.getOutPathFor("archive") + ":@")

    def _renderFrames(self):
        for framenum in range(self._frames[0], self._frames[1]+1):
            self._rndrdoc.render(self._renderer, framenum)

    def _verifyFrameRange(self, framerange=None):
        self._frames = self._assetman.getFrameRange()
        if framerange:
            if len(framerange) != 2:
                raise RndrJobException("invalid framerange: " + str(framerange))

            if framerange[0] < 0 or framerange[1] < 0:
                raise RndrJobException("invalid framerange: " + str(framerange))

            if framerange[1] > self._frames[1]:
                framerange[1] = self._frames[1]
            self._frames = framerange

    def setOutputPath(self, path):
        self._assetman.outputpath = path

    def createOutDirs(self):
        self._assetman.createOutDirs()

    def makeAssetsRelative(self):
        self.updateAssets()

    def updateAssets(self):
        self._assetman.updateAssets()

    def copyAssetToDirectory(self, asset):
        self._assetman._copyAssetToDirectory(asset)

    def _startRenderer(self, libName=None):
        self._renderer = ri.loadRI(libName)
        self._renderer.RiBegin(ri.RI_NULL)

    def _stopRenderer(self):
        self._renderer.RiEnd()
