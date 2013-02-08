from chronorender.cr_object import Object
from chronorender.cr_types import intlist

class MovieException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Movie(Object):
    @staticmethod
    def getTypeName():
        return "movie"

    def getBaseName(self):
        return Movie.getTypeName()

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)

        self.output     = self.getVar('output', kwargs)
        self.outdir     = self.getVar('outdir', kwargs)
        self.framerate  = self.getVar('framerate', kwargs)
        self.format     = self.getVar('format', kwargs)
        self.res        = self.getVar('resolution', kwargs)
        self.codec      = self.getVar('codec', kwargs)
        self.bitrate    = self.getVar('bitrate', kwargs)
        self.vpreset    = self.getVar('vpreset', kwargs)

    def _initMembersDict(self):
        super(Movie, self)._initMembersDict()

        self._members['output']       = [str, "default.mp4"]
        self._members['outdir']       = [str, ""]
        self._members['framerate']    = [int, 24]
        self._members['format']       = [str, 'default']
        self._members['resolution']   = [intlist, [640, 480]] 
        self._members['codec']        = [str, 'default']
        self._members['bitrate']      = [str, 'default']
        self._members['vpreset']      = [str, 'default']

    def setInputFile(self, filepath):
        return

    def encode(self):
        return

def build(**kwargs):
    return Movie(**kwargs)
