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

    def find(self, assetname):
        if os.path.exists(assetname): return assetname
        assetname = os.path.basename(assetname)
        cwd = os.getcwd()
        paths = [os.getcwd()]
        paths.extend(self._searchpaths)
        for path in paths:
            for root, dirs, files in os.walk(path):
                if assetname in files:
                    return os.path.join(root, assetname)
        raise AssetNotFoundException(self, 'could not find: ' + assetname)

    def addPathsStr(self, path_string, delim=':'):
        return

    def addPathsList(self, path_list):
        return

    def getSearchPaths(self):
        return self._searchpaths
