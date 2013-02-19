import os

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
      self._searchpaths = Finder.searchpaths

    def __str__(self):
        return str(self._searchpaths)

    def find(self, assetpath):
        if os.path.exists(assetpath): return assetpath
        assetname = os.path.basename(assetpath)
        cwd = os.getcwd()
        cwd_parent = os.path.dirname(cwd)
        paths = [cwd, cwd_parent]
        paths.extend(self._searchpaths)
        for path in paths:
            for root, dirs, files in os.walk(path):
                if assetname in files:
                    return os.path.join(root, assetname)

                fdir = self._findDir(root, assetpath)
                if fdir: return fdir
        raise AssetNotFoundException(self, 'could not find: ' + assetname)

    def _findDir(self, searchpath, assetdir):
        adir, ext = os.path.splitext(assetdir)
        if ext:
            adir = os.path.dirname(adir)
        if searchpath.endswith(adir):
            return searchpath

    def addPathsStr(self, path_string, delim=':'):
        return

    def addPathsList(self, path_list):
        return

    def getSearchPaths(self):
        return self._searchpaths
