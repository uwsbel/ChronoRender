import os, shutil, imghdr, subprocess, glob
import chronorender.ri.rmanlibutil as riutil
from chronorender.finder import FinderFactory, AssetNotFoundException

class RndrJobAssetManager(object):
    def __init__(self, outpath, rndrdoc, relative=True):
        self.outputpath = outpath
        self.rndrdoc    = rndrdoc
        self.relative   = relative
        self.finder     = self._createAssetFinder()
        self.outputdirs    = {  'root' : '',
                                'output': 'OUTPUT', 
                                'shader': 'SHADERS', 
                                'script': 'SCRIPTS', 
                                'archive': 'ARCHIVES', 
                                'log':'LOG',
                                'texture': 'TEXTURES' }

    class Helper(object):
        def __init__(self, findfunc, outfunc, outpath):
            self.findfunc = findfunc
            self.outfunc = outfunc
            self.outpath = outpath

        def find(self, filename):
            return self.findfunc(filename)

        def getOutPathFor(self, filetype):
            return self.outfunc(filetype)


    def find(self, filename):
        return self.finder.find(filename)

    def getOutPathFor(self, typename):
        if self.relative:
            return self.outputdirs[typename]
        else: 
            return os.path.join(self.outputpath, self.outputdirs[typename])
        
    def createOutDirs(self):
        if not os.path.exists(self.outputpath): 
            os.makedirs(self.outputpath)

        dirs = []
        for key, val in self.outputdirs.iteritems():
            dirs.append(os.path.join(self.outputpath,val))
        for di in dirs:
            if not os.path.exists(di):
                os.makedirs(di)

    def makeAssetsRelative(self):
        self._updateAssets()

    def updateAssets(self):
        prevdir = os.getcwd()

        try:
            os.chdir(self.outputpath)

            helper = RndrJobAssetManager.Helper(
                    self.finder.find, 
                    self.getOutPathFor,
                    self.outputpath)
            # paths = self.rndrdoc.resolveAssets(self._createAssetFinder(), self.outputpath)
            paths = self.rndrdoc.resolveAssets(helper)
            currassets = self._getCurrentAssets()
            for path in paths:
                if path not in currassets:
                    self._copyAssetToDirectory(path)
        finally:
            os.chdir(prevdir)

    def compileShaders(self, renderer):
        if renderer == None:
            return

        sdrc = riutil.sdrcFromRenderer(renderer)

        if sdrc == None:
            return

        prevdir = os.getcwd()
        try:
            os.chdir(self.outputpath)
            os.chdir(self.getOutPathFor('shader'))
            shdrs = glob.glob('./*.sl')
            prog = [sdrc]
            prog.extend(shdrs)
            subprocess.call(prog)
        finally:
            os.chdir(prevdir)

    def getFrameRange(self):
        return self.rndrdoc.getFrameRange()

    def _createAssetFinder(self):
        if self.relative:
            return FinderFactory.build(self.rndrdoc.getSearchPaths(), self.outputpath)
        return FinderFactory.build(self.rndrdoc.getSearchPaths())

    def _copyAssetToDirectory(self, asset):
        filename, ext = os.path.splitext(asset)
        try:
            if ext == ".sl":
                shutil.copy2(asset, self.getOutPathFor('shader'))
            elif ext == ".py":
                shutil.copy2(asset, self.getOutPathFor('script'))
            elif ext == ".rib":
                shutil.copy2(asset, self.getOutPathFor('archive'))
            elif imghdr.what(asset) != None:
                shutil.copy2(asset, self.getOutPathFor('texture'))
        except:
            pass

    def _getCurrentAssets(self):
        out = []
        out.extend(self._dirWalkToList(self.getOutPathFor('shader')))
        out.extend(self._dirWalkToList(self.getOutPathFor('script')))
        out.extend(self._dirWalkToList(self.getOutPathFor('archive')))
        out.extend(self._dirWalkToList(self.getOutPathFor('texture')))
        return out

    def _dirWalkToList(self, path):
        out = []
        for root, dirs, files in os.walk(path):
            out.extend([os.path.join(root,f) for f in files])
        return out
