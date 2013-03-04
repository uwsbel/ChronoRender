try:
    import numpy as np
except ImportError:
    print "No numpy installed, cannot use MusicViz RenderObject"

import wave, struct
from chronorender.renderobject import RenderObject

class MusicViz(RenderObject):
    @staticmethod
    def getTypeName():
        return "musicviz"

    def __init__(self, *args, **kwargs):
        super(MusicViz,self).__init__(*args, **kwargs)

        self.wavfile = self.getVar('wavfile', kwargs)
        self._breadwav = False
        self._wavdata  = None
        self._wavstats = {}

    def _initMembersDict(self):
        super(MusicViz,self)._initMembersDict()
        self._members['wavfile'] = [string, '']

    def updateMembers(self):
        self.setMember('wavfile', self.filename)

    def resolveAssets(self, assetman):
        out = super(MusicViz, self).resolveAssets(assetman)
        self.wavfile = assetman.find(self.wavfile)
        out.append(self.wavfile)
        return out

    def render(self, rib, *args, **kwargs):
        if not self._breadwav:
            self._readWavData()
            self._breadwav = True

        self.color = self._computeCurrColor(kwargs['framenumber'])
        super(MusicViz, self).render(rib, *args, **kwargs)

    def _readWavData(self):
        wav = wave.open(self.wavfile, 'r')
        params = wav.getparams()
        self._wavstats = {
                'nchannels' : params[0], 'sampwidth' : params[1],
                'framerate' : params[2], 'comptype' : params[3], 
                'compname' : params[4]}
        wav.close()

    def _computeCurrColor(self, framenum):
        return [1.0, 1.0, 1.0]

    def _getAvgFreqRange(self, framenum):
        return

    def _getSpectrum(self, framenum):
        return

def build(**kwargs):
    return MusicViz(**kwargs)
