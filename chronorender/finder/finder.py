import os, sys

class AssetNotFoundException(Exception):
    def __init__(self, finder, value):
        self.finder = finder
        self.value = value
    def __str__(self):
        msg = self.value + ' on paths: ' + str(self.finder)
        return repr(msg)

class Finder(object):
    searchpaths = ""

    def __init__(self, paths, relative=None):
        # self._searchpaths = Finder.searchpaths
        self._searchpaths = []

    def __str__(self):
        return str(self._searchpaths)

    def find(self, assetpath):
        if os.path.exists(assetpath): return assetpath

        assetpath = os.path.normpath(assetpath)

        if sys.platform.startswith('linux'):
            # try linux fs 
            ap = assetpath.replace('\\','/')
        else:
            # try windows fs
            ap = assetpath.replace('/','\\')

        out = self._findFile(ap)
        if out: return out
        out = self._findDir(ap)
        if out: return out

        raise AssetNotFoundException(self, 'could not find: ' + ap)

    def _buildPaths(self):
        cwd = os.getcwd()
        cwd_parent = os.path.dirname(cwd)
        paths = [cwd, cwd_parent]
        paths.extend(self._searchpaths)
        return paths

    def _findDir(self, assetpath):
        paths = self._buildPaths()
        assetname = os.path.basename(assetpath)
        for path in paths:
            for root, dirs, files in os.walk(path):
                outdir = self._findDirHelper(root, assetpath)
                if outdir: return outdir
        return None

    def _findDirHelper(self, root, assetpath):
        assetdir, base = os.path.split(assetpath)
        if root.endswith(assetdir): return os.path.join(root, base)
        return None

    def _findFile(self, assetpath):
        paths = self._buildPaths()
        assetname = os.path.basename(assetpath)
        for path in paths:
            for root, dirs, files in os.walk(path):
                outfile = self._findFileHelper(root, files, assetpath)
                if outfile: return outfile
        return None

    def _findFileHelper(self, root, files, assetpath):
        fdir, assetname = os.path.split(assetpath)
        if assetname not in files: return None
        if root.endswith(fdir):
            return os.path.join(root, assetname)
        return None

    def addPathsStr(self, path_string, delim=':'):
        return

    def addPathsList(self, path_list):
        return

    def getSearchPaths(self):
        return self._searchpaths
