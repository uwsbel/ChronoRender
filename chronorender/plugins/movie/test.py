import subprocess, os.path

import chronorender.cr_utils as crutils
from chronorender.movie import Movie, MovieException

class MOVIETEST(Movie):
    _ffmpeg = 'ffmpeg'

    @staticmethod
    def getTypeName():
        return 'TEST'

    def __init__(self, *args, **kwargs):
        super(MOVIETEST, self).__init__(*args, **kwargs)

        self._fileexpr = ""
        self._convertDefaults()

    def _initMembersDict(self):
        super(MOVIETEST, self)._initMembersDict()

    def setInputFile(self, filepath):
        vals = filepath.split('.')
        index = self._findPadding(vals)
        if not index:
            raise MovieException('no padding in filename: ' + filepath)

        padding = self._evalPadding(vals[index])

        out = vals[0]
        for i in range(1, len(vals)):
            if i == index:
                out += ".%0" + str(padding) + "d"
                #out += ".*"
            else:
                out += "." + vals[i]
        self._fileexpr = out

    def encode(self):
        exe = self._verifyExecutable()
        subprocess.call(self._getArgsList())

    def _findPadding(self, vals):
        for i in range(0, len(vals)):
            v = vals[i]
            if v.isdigit():
                return i
        return None

    def _evalPadding(self, padding):
        return len(str(padding))

    def _verifyExecutable(self):
        exe = crutils.which(MOVIETEST._ffmpeg)
        if not exe:
            raise MovieException(MOVIETEST._ffmpeg + " not installed on system")
        return exe

    def _getArgsList(self):
        args = [MOVIETEST._ffmpeg]

        args.extend(['-loglevel', 'panic'])
        args.extend(['-f', self.format])
        #args.extend(['-pattern_type', 'glob'])
        #args.extend(['-i', "\'" + self._fileexpr + "\'"])
        args.extend(['-i', self._fileexpr])
        args.extend(['-r', str(self.framerate)])
        args.extend(['-vcodec', self.codec])
        #args.extend(['-vpre', self.vpreset])
        args.extend(['-s', MOVIETEST._getFormattedRes(self.res)])
        args.extend(['-b', self.bitrate])
        args.extend(['-crf', str(15)])
        args.append(self._getOutFilePath())

        return args

    def _convertDefaults(self):
        if self.format == 'default':
            self.format = 'image2'
        if self.codec == 'default':
            self.codec = 'libx264'
        if self.bitrate == 'default':
            self.bitrate = '4M'
        if self.vpreset == 'default':
            self.vpreset = 'normal'

    @staticmethod
    def _getFormattedRes(res):
        if len(res) != 2:
            raise MovieException('invalid resolution: ' + str(res))
        return str(res[0]) + 'x' + str(res[1])
        #return "WxH"

    def _getOutFilePath(self):
        return os.path.join(self.outdir, self.output)

def build(**kwargs):
    return MOVIETEST(**kwargs)
