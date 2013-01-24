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

    def resolveAssets(self, assetman):
        out = super(File, self).resolveAssets(assetman)

        inputfile = assetman.find(self.filename)
        outname = self._getNewFilename()

        try:
            # already exists?
            self.filename = assetman.find(outname)
        except Exception:
            conv = ConverterFactory.build(inputfile)
            outpath = assetman.getOutPathFor('archive')
            outfile = path.join(outpath, outname)
            self.filename = conv.convert(outfile,
                    shader_outpath = assetman.getOutPathFor('shader'),
                    texture_outpath = assetman.getOutPathFor('texture'),
                    archive_outpath = assetman.getOutPathFor('archive')
                    )

        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        rib.RiReadArchive(self.filename)

    def _getNewFilename(self):
        filedir, filename = path.split(self.filename)
        filename, ext = path.splitext(filename)
        filename = filename + '.rib'
        return filename

def build(**kwargs):
    return File(**kwargs)
