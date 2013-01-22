import os.path as path

from chronorender.geometry import Geometry
from chronorender.converter import ConverterFactory

class File(Geometry):
    @staticmethod
    def getTypeName():
        return "file"

    def __init__(self, *args, **kwargs):
        super(File,self).__init__(*args, **kwargs)
        self.filename = self.getMember('filename')

    def _initMembersDict(self):
        super(File,self)._initMembersDict()
        self._members['filename'] = [str, '']

    def resolveAssets(self, finder, outpath):
        out = super(File, self).resolveAssets(finder, outpath)
        outname = self._getNewFilename(outpath)

        try:
            self.filename = finder.find(outname)
        except Exception:
            conv = ConverterFactory.build(self.filename)
            self.filename = conv.convert(outname)

        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        rib.RiReadArchive(self.filename)

    def _getNewFilename(self, outpath):
        filedir, filename = path.split(self.filename)
        filename, ext = path.splitext(filename)
        filename = filename + '.rib'
        return path.join(outpath, filename)

def build(**kwargs):
    return File(**kwargs)
