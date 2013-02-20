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

        paths = self._buildPaths()
        assetname = os.path.basename(assetpath)
        for path in paths:
            for root, dirs, files in os.walk(path):
                outfile = self._findFile(root, files, assetname)
                outfile = self._findDir(root, assetpath)
                if outfile: return outfile
        raise AssetNotFoundException(self, 'could not find: ' + assetname)

    def _buildPaths(self):
        cwd = os.getcwd()
        cwd_parent = os.path.dirname(cwd)
        paths = [cwd, cwd_parent]
        paths.extend(self._searchpaths)
        return paths

    def _findDir(self, root, assetpath):
        assetdir, ext = os.path.splitext(assetpath)
        if ext: return None
        # assetdir = os.path.dirname(assetpath)
        if root.endswith(assetdir): return root
        return None

    def _findFile(self, root, files, assetname):
        if assetname in files:
            return os.path.join(root, assetname)
        return None

    def addPathsStr(self, path_string, delim=':'):
        return

    def addPathsList(self, path_list):
        return

    def getSearchPaths(self):
        return self._searchpaths
