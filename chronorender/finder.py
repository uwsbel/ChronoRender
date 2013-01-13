import os

class AssetNotFoundException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Finder():
    def __init__(self, paths):
        self._paths = paths

    def find(self, assetname):
        for path in self._paths:
            testpath = path + assetname
            if os.path.exists(testpath):
                return testpath
        raise AssetNotFoundException('could not find: ' + assetname)
