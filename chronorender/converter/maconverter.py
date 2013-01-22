from cgkitconverter import CGKitConverter

try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.maimport import *

class MAConverter(CGKitConverter):
    def __init__(self, src):
        super(MAConverter, self).__init__(src)
        self._reader = MAImporter()
