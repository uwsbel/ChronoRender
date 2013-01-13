# contains all assests needed to start a render job
from rndr_settings import RndrSettings

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():
    def __init__(self, *args, **kwargs):
        self.settings   = RndrSettings()
        self.rndrpasses = []
        self.shaders    = []
        self.geometry   = []
        self.lighting   = 'default.rib'
        self.scene      = 'default.rib'

    def _resolveAssetPaths(self):
        return
