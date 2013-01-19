from cr_object import Renderable

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

        self.name = self.getMember('name')

    def _initMembersDict(self):
        self._members['name']       = [str, 'default']

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, **kwargs):
        rib.write(self.name)

def build(**kwargs):
    return Settings(**kwargs)
