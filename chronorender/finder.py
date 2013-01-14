import os

class AssetNotFoundException(Exception):
    def __init__(self, finder, value):
        self.finder = finder
        self.value = value
    def __str__(self):
        msg = self.value + ' on paths: ' + str(self.finder)
        return repr(msg)

class Finder():
    def __init__(self, paths):
        self._searchpaths = self._resolveToAbsolutePaths(paths)

    def __str__(self):
        return str(self._searchpaths)

    def find(self, assetname):
        for path in self._searchpaths:
            testpath = path + assetname
            if os.path.exists(testpath):
                return testpath
        raise AssetNotFoundException(self, 'could not find: ' + assetname)

    def addPathsStr(self, path_string, delim=':'):
        paths = path_string.split(delim)
        self._searchpaths += self._resolveToAbsolutePaths(paths)

    def addPathsList(self, path_list):
        self._searchpaths += self._resolveToAbsolutePaths(path_list)

    def getSearchPaths(self):
        return self._searchpaths

    def _resolveToAbsolutePaths(self, paths):
        resolved_paths = []
        for i in range(0,len(paths)):
            if os.path.exists(paths[i]):
                resolved_paths.append(os.path.abspath(paths[i]) + os.sep)
        return resolved_paths
