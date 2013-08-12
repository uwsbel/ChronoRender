import os, shutil, imghdr, subprocess, glob
import chronorender.ri.rmanlibutil as riutil
from chronorender.finder import FinderFactory, AssetNotFoundException

class CRAssetInfo(object):
    def __init__(self, outpath='.', relative=True, jobname='job'):
        self.outputpath = outpath
        self.relative   = relative
        self.jobname = jobname
        jobdir = os.path.dirname(self.jobname)
        self.outputdirs = { 'root' : '',
                            'job'  : self.jobname,
                            'data' :  os.path.join(self.jobname, 'data'),
                            'output': os.path.join(self.jobname,'images'),
                            'shader': os.path.join(self.jobname,'shaders'),
                            'rib'   : os.path.join(self.jobname, 'rib'),
                            'script': os.path.join(jobdir, 'scripts'), 
                            'archive': os.path.join(jobdir, 'ribarchives'),
                            'log':    os.path.join(jobdir, 'log'),
                            'texture': os.path.join(jobdir, 'textures') }

    @staticmethod
    def _getFileType(asset):
        filename, ext = os.path.splitext(asset)
        if ext == ".sl":
            return 'shader'
        elif ext == ".slx": #TODO: does returning 'shader' for slo/x work?
            return 'shader'
        elif ext == ".slo":
            return 'shader'
        elif ext == ".py":
            return 'script'
        elif ext == ".rib":
            return 'archive'
        elif imghdr.what(asset) != None:
            return 'texture'
        return ''

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

    def compileShaders(self, renderer):
        if renderer == None:
            return

        sdrc = riutil.sdrcFromRenderer(renderer)
        if not sdrc:
            return

        prevdir = os.getcwd()
        try:
            os.chdir(self.outputpath)
            os.chdir(self.getOutPathFor('shader'))
            shdrs = glob.glob('./*.sl')
            prog = [sdrc]
            prog.extend(shdrs)
            if len(prog) >= 2:
                subprocess.call(prog)
        finally:
            os.chdir(prevdir)

    def convertTextures(self, renderer):
        if renderer == None:
            return

        txmk = riutil.txmkFromRenderer(renderer)
        if not txmk:
            return

        prevdir = os.getcwd()
        try:
            os.chdir(self.outputpath)
            os.chdir(self.getOutPathFor('texture'))
            texs = glob.glob('./*')
            intexs = []
            for tex in texs:
                path, f = os.path.split(tex)
                name, ext = os.path.splitext(f)
                if ext != '.tex':
                    intexs.append([tex, name + '.tex'])
            for tex in intexs:
                exe = [txmk]
                exe.extend(tex)
                subprocess.call(exe)
        finally:
            os.chdir(prevdir)

    def copyAssetToDirectory(self, asset):
        filename, ext = os.path.splitext(asset)
        prevdir = os.getcwd()
        try:
            os.chdir(self.outputpath)
            atype = CRAssetInfo._getFileType(asset)
            path = self.getOutPathFor(atype)
            shutil.copy2(asset, path)
        except:
            pass
        finally:
            os.chdir(prevdir)

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

    def copyAssetsToJobDir(self, paths):
        currassets = self._getCurrentAssets()
        for path in paths:
            if path not in currassets:
                self.copyAssetToDirectory(path)

    def createAssetFinder(self, searchpaths):
        if self.relative:
            return FinderFactory.build(searchpaths, self.outputpath)
        return FinderFactory.build(searchpaths)
