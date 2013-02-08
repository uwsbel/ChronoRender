import os, shutil, imghdr, subprocess, glob
from chronorender.cr_assetinfo import CRAssetInfo

class RndrJobAssetManager(object):
    def __init__(self, outpath, rndrdoc, relative=True, jobname='job'):
        self.relative   = relative
        self.assetinfo  = CRAssetInfo(outpath=outpath, relative=self.relative, jobname=jobname)
        self.rndrdoc    = rndrdoc
        self.finder     = self.assetinfo.createAssetFinder(rndrdoc.getSearchPaths())

        self._assets    = { 'data': [],
                            'shader':  [],
                            'script':  [],
                            'archive': [],
                            'texture': [] }

    class Helper(object):
        def __init__(self, findfunc, outfunc, outpath):
            self.findfunc = findfunc
            self.outfunc = outfunc
            self.outpath = outpath

        def find(self, filename):
            return self.findfunc(filename)

        def getOutPathFor(self, filetype):
            return self.outfunc(filetype)

        def convertTextureName(self, name):
            return os.path.splitext(name)[0] + '.tex'


    def find(self, filename):
        return self.finder.find(filename)

    def getFrameRange(self):
        return self.rndrdoc.getFrameRange()

    def getOutPathFor(self, typename):
        return self.assetinfo.getOutPathFor(typename)

    def setOutPath(self, path):
        self.assetinfo.outputpath = path

    def copyAssetToDirectory(self, asset):
        self.assetinfo.copyAssetToDirectory(asset)

    def createOutDirs(self):
        self.assetinfo.createOutDirs()

    def makeAssetsRelative(self):
        self._updateAssets()

    def updateAssets(self):
        prevdir = os.getcwd()

        try:
            os.chdir(self.assetinfo.outputpath)
            helper = RndrJobAssetManager.Helper(
                    self.finder.find, 
                    self.assetinfo.getOutPathFor,
                    self.assetinfo.outputpath)
            paths = self.rndrdoc.resolveAssets(helper)
            self._initManagerAssetsDict(paths)
            self.assetinfo.copyAssetsToJobDir(paths)
        finally:
            os.chdir(prevdir)

    def compileShaders(self, renderer):
        self.assetinfo.compileShaders(renderer)

    def convertTextures(self, renderer):
        self.assetinfo.convertTextures(renderer)

    def _initManagerAssetsDict(self, paths):
        self._clearManagerAssetsDict()
        for asset in paths:
            atype = CRAssetInfo._getFileType(asset)
            self._assets[atype].append(asset)

    def _clearManagerAssetsDict(self):
        for key, val in self._assets.iteritems():
            del val[0:len(val)]
