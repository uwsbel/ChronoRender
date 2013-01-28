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
        self.filepath = ""

    def _initMembersDict(self):
        super(File,self)._initMembersDict()
        self._members['filename'] = [str, '']

    def resolveAssets(self, assetman):
        out = super(File, self).resolveAssets(assetman)

        self.filepath = assetman.find(self.filename)
        outname = self._getNewFilename()

        try:
            # already exists?
            self.filename = assetman.find(outname)
            out = self.filename
        except Exception:
            out = self._generateRIBArchive(self.filepath, 
                    assetman.getOutPathFor('archive'),
                    assetman.getOutPathFor('shader'), 
                    assetman.getOutPathFor('texture'))

        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        rib.RiReadArchive(self.filename)

    def _generateRIBArchive(self, inputfile, outname,
            outpath_arc, outpath_sdr, outpath_tex):
        conv = ConverterFactory.build(inputfile)
        outpath = outpath_arc
        outfile = path.join(outpath, outname)
        self.filename = conv.convert(outfile,
                shader_outpath = outpath_sdr,
                texture_outpath = outpath_tex,
                archive_outpath = outpath_arc)
        return outfile

    def _getNewFilename(self):
        filedir, filename = path.split(self.filename)
        filename, ext = path.splitext(filename)
        filename = filename + '.rib'
        return filename

def build(**kwargs):
    return File(**kwargs)
