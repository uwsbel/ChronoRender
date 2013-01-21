import os
import chronorender.cr_utils as cr_utils
from finder import Finder, AssetNotFoundException

class FinderAbs(Finder):
    def __init__(self, paths, relative=None):
        self._searchpaths = self._resolveToAbsolutePaths(paths, relative)

    def __str__(self):
        return str(self._searchpaths)

    def addPathsStr(self, path_string, delim=':'):
        paths = path_string.split(delim)
        self._searchpaths += self._resolveToAbsolutePaths(paths)

    def addPathsList(self, path_list):
        self._searchpaths += self._resolveToAbsolutePaths(path_list)

    def getSearchPaths(self):
        return self._searchpaths

    def _resolveToAbsolutePaths(self, paths, relativeto=None):
        resolved_paths = []
        for path in paths:
            path = cr_utils.getAbsPathRelativeTo(path, relativeto) if relativeto else path
            if os.path.exists(path):
                if not os.path.isdir(path):
                    path = os.path.split(path)[0]
                out = os.path.abspath(path)
                resolved_paths.append(out)
        return resolved_paths
