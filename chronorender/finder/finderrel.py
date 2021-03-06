import os
import chronorender.cr_utils as cr_utils
from finder import Finder, AssetNotFoundException

class FinderRel(Finder):
    def __init__(self, paths, relative):
        self._searchpaths = FinderRel._resolveToAbsolutePaths(paths, relative)
        self._relative = relative

    def __str__(self):
        return str(self._searchpaths)

    def addPathsStr(self, path_string, delim=':'):
        paths = path_string.split(delim)
        self._searchpaths.extend(paths)

    def addPathsList(self, path_list):
        self._searchpaths.extend(path_list)

    def getSearchPaths(self):
        return self._searchpaths

    @staticmethod
    def _resolveToRelative(paths, relative):
        resolved_paths = []
        for path in paths:
            path = os.path.relpath(path, relative)
            if os.path.exists(path):
                if not os.path.isdir(path):
                    path = os.path.split(path)[0]
                resolved_paths.append(path)
        return resolved_paths

    @staticmethod
    def _resolveToAbsolutePaths(paths, relativeto=None):
        resolved_paths = []
        for path in paths:
            path = cr_utils.getAbsPathRelativeTo(path, relativeto) if relativeto else path
            if os.path.exists(path):
                if not os.path.isdir(path):
                    path = os.path.split(path)[0]
                out = os.path.abspath(path)
                resolved_paths.append(out)
        return resolved_paths
