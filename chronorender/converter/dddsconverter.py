from cgkitconverter import CGKitConverter

try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.dddsimport import *

class DDDSConverter(CGKitConverter):
    def __init__(self, src):
        super(DDSConverter, self).__init__(src)
        self._reader = DDSImporter()
