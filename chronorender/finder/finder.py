import os

class AssetNotFoundException(Exception):
    def __init__(self, finder, value):
        self.finder = finder
        self.value = value
    def __str__(self):
        msg = self.value + ' on paths: ' + str(self.finder)
        return repr(msg)

class Finder(object):
    def __str__(self):
        return str(self._searchpaths)

    def find(self, assetname):
        if os.path.exists(assetname): return assetname
        for path in self._searchpaths:
            # TODO GOOD idea to walk recursively?
            for root, dirs, files in os.walk(path):
                if assetname in files:
                    return os.path.join(root, assetname)
            # testpath = os.path.join(path,assetname)
            # if os.path.exists(testpath):
                # return testpath
        raise AssetNotFoundException(self, 'could not find: ' + assetname)

    def addPathsStr(self, path_string, delim=':'):
        return

    def addPathsList(self, path_list):
        return

    def getSearchPaths(self):
        return self._searchpaths
