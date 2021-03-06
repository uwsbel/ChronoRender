from cgkitconverter import CGKitConverter

try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.objimport import OBJImporter

class OBJConverter(CGKitConverter):
    def __init__(self, src):
        super(OBJConverter, self).__init__(src)
        self._reader = OBJImporter()
