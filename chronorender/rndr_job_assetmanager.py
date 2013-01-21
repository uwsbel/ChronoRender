import os, shutil, imghdr
from chronorender.finder import FinderFactory, AssetNotFoundException

class RndrJobAssetManager(object):
    def __init__(self, outpath):
        self.outputpath = outpath
        self.relative = True
        self.outputdirs    = {  'root' : '',
                                'output': 'OUTPUT', 
                                'shader': 'SHADERS', 
                                'script': 'SCRIPTS', 
                                'archive': 'ARCHIVES', 
                                'log':'LOG',
                                'texture': 'TEXTURES' }

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

    def makeAssetsRelative(self, rndrdoc):
        self.updateAssets(rndrdoc)

    def updateAssets(self, rndrdoc):
        prevdir = os.getcwd()
        os.chdir(self.outputpath)
        paths = rndrdoc.resolveAssets(self.createAssetFinder(rndrdoc))
        currassets = self._getCurrentAssets()
        for path in paths:
            if path not in currassets:
                self._copyAssetToDirectory(path)
        os.chdir(prevdir)

    def createAssetFinder(self, rndrdoc):
        if self.relative:
            return FinderFactory.build(rndrdoc.getSearchPaths(), self.outputpath)
        return FinderFactory.build(rndrdoc.getSearchPaths())

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
