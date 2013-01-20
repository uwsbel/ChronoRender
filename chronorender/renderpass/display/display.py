from cr_object import Renderable

class DisplayException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Display(Renderable):

    @staticmethod
    def getTypeName():
        return "display"

    def __init__(self, *args, **kwargs):
        super(Display,self).__init__(*args, **kwargs)

        self.output     = self.getMember('output')
        self.outtype    = self.getMember('outtype')
        self.mode       = self.getMember('mode')

    def _initMembersDict(self):
        super(Display, self)._initMembersDict()
        self._members['output']     = [str, 'default']
        self._members['outtype']    = [str, 'file']
        self._members['mode']       = [str, 'rgba']

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        rib.RiDisplay(self.output, self.outtype,self.mode)


def build(**kwargs):
    return Display(**kwargs)
