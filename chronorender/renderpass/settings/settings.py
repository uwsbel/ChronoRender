from chronorender.cr_renderable import Renderable
from chronorender.renderpass.display import Display

from chronorender.cr_types import floatlist, intlist

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
        self.displays   = self.getMember(Display.getTypeName())

    def _initMembersDict(self):
        super(Settings, self)._initMembersDict()
        self._members['name']                       = [str, 'default']
        self._members['resolution']                 = [intlist, [640, 480]]
        self._members['interpolation']              = [str, 'smooth']
        self._members['shadingrate']                = [float, 4.0]
        self._members['pixelsamples']               = [intlist, [4, 4]]
        self._members[Display.getTypeName()]   = [Display, []]

    def render(self, rib, outpath='', postfix='', **kwargs):
        rib.Format(self.resolution[0], self.resolution[1], 1)
        rib.PixelSamples(self.samples[0],self.samples[1])
        rib.ShadingRate(self.rate)
        rib.ShadingInterpolation(self.interp)

        for d in self.displays:
            # d.render(rib, outpath, postfix, **kwargs)
            d.render(rib, outpath, postfix, **kwargs)

def build(**kwargs):
    return Settings(**kwargs)
