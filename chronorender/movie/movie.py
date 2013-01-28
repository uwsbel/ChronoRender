from cr_object import Object

class Movie(Object):
    @staticmethod
    def getTypeName():
        return "movie"

    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)

        self.framerate = self.getMember('framerate')
        self.format = self.getMember('format')
        self.res= self.getMember('resolution')
        self.codec = self.getMember('codec')
        self.bitrate = self.getMember('bitrate')
        self.vpreset = self.getMember('vpreset')

    def _initMembersDict(self):
        super(Movie, self)._initMembersDict()

        self._members['framerate']  = [int, 24]
        self._members['format']     = [str, 'default']
        self._members['resolution']   = [list, [640, 480]] 
        self._members['codec']        = [str, 'default']
        self._members['bitrate']      = [str, 'default']
        self._members['vpreset']      = [str, 'default']

    def encode(self):
        return

def build(**kwargs):
    return Movie(**kwargs)
