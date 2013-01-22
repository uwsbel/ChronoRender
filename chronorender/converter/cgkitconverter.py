from os import path
from converter import Converter
try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.targetcamera import TargetCamera
from cgkit.pluginmanager import *

class CGKitConverter(Converter):
    def __init__(self, src):
        super(CGKitConverter, self).__init__(src)
        self._reader = None
        self._exporter = CGKitConverter._linkRIBExporter()
        self._dummy = TargetCamera( pos = (3,2,2), target = (0,0,0))

    def convert(self, dest):
        self._reader.importFile(self._src)
        self._exporter.exportFile(dest)
        del self._reader
        del self._exporter
        del self._dummy

    @staticmethod
    def _linkRIBExporter():
        pm = PluginManager()

        moddir = path.dirname(path.abspath(__file__))
        mod = path.join(moddir, 'crender_ribexporter.py')
        pdesc = pm.importPlugin(mod)

        objdesc = pm.findObject('crender_ribexporter.CRenderRIBExporter')
        cls = objdesc.object
        return cls()
