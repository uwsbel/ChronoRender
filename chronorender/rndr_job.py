import datetime, os, logging, glob, multiprocessing

import chronorender.metadata as md
import chronorender.rndr_doc as rd
import chronorender.ri as ri
from chronorender.rndr_job_assetmanager import RndrJobAssetManager

workerpool = multiprocessing.Pool()

class RndrJobException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrJob():
    def __init__(self, infile, factories):
        self._metadata      = md.MetaData(infile)
        self._rndrdoc       = rd.RndrDoc(factories, self._metadata)
        self._rootdir       = os.path.abspath(os.path.split(self._metadata.filename)[0])
        self._timecreated   = datetime.datetime.now()
        self._frames        = self._rndrdoc.getFrameRange()
        self._assetman      = RndrJobAssetManager(self._rootdir, self._rndrdoc)
        self._renderer      = None

    def run(self, renderer=None, framerange=None):
        self._assetman.createOutDirs()
        prevdir = os.getcwd()
        try:
            os.chdir(self._rootdir)
            self._assetman.updateAssets()
            self._assetman.compileShaders(renderer)
            self._render(renderer)
        finally:
            os.chdir(prevdir)

    def _render(self, renderer=None):
        self._startRenderer(ri.rmanlibutil.libFromRenderer(renderer))
        self._renderOptions()
        self._renderFrames()
        self._stopRenderer()

    def _renderOptions(self):
        self._renderer.RiOption("searchpath", "shader",
                self._assetman.getOutPathFor("shader") + ":@")
        self._renderer.RiOption("searchpath", "procedural",
                self._assetman.getOutPathFor("script") + ":@")
        self._renderer.RiOption("searchpath", "texture",
                self._assetman.getOutPathFor("texture") + ":@")
        self._renderer.RiOption("searchpath", "archive",
                self._assetman.getOutPathFor("archive") + ":@")

    def _renderFrames(self):
        for framenum in range(self._frames[0], self._frames[1]+1):
            self._rndrdoc.render(self._renderer, framenum)

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
