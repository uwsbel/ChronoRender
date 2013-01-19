from cr_object import Renderable

import renderpass.display as disp
from cr_types import floatlist, intlist

class SettingsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Settings(Renderable):

    @staticmethod
    def getTypeName():
        return "settings"

    def __init__(self, *args, **kwargs):
        super(Settings,self).__init__(*args, **kwargs)

        self.name       = self.getMember('name')
        self.resolution = self.getMember('resolution')
        self.interp     = self.getMember('interpolation')
        self.rate       = self.getMember('shadingrate')
        self.samples    = self.getMember('pixelsamples')
        self.displays   = self.getMember('display')

    def _initMembersDict(self):
        self._members['name']           = [str, 'default']
        self._members['resolution']     = [intlist, [640, 480]]
        self._members['interpolation']  = [str, 'smooth']
        self._members['shadingrate']    = [float, 4.0]
        self._members['pixelsamples']   = [intlist, [4, 4]]
        self._members['display']        = [disp.Display, []]

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        rib.RiFormat(self.resolution[0], self.resolution[1], 1)
        rib.RiPixelSamples(self.samples[0],self.samples[1])
        rib.RiShadingRate(self.rate)
        rib.RiShadingInterpolation(self.interp)

        for d in self.displays:
            d.render(rib, **kwargs)

def build(**kwargs):
    return Settings(**kwargs)
