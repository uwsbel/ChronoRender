from cgkitconverter import CGKitConverter

try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.plyimport import *

class PLYConverter(CGKitConverter):
    def __init__(self, src):
        super(PLYConverter, self).__init__(src)
        self._reader = PLYImporter()
