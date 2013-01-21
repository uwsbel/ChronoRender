import sys
from os import path
from converter import Converter

try:
    import cgkit
except ImportError:
    import chronrender.thirdparty.cgkit as cgkit

from cgkit.targetcamera import TargetCamera
from cgkit.objimport import *
from cgkit.pluginmanager import *
from cgkit.ribexport import *

class OBJConverter(Converter):
    def __init__(self):
        self._reader = OBJImporter()
        self._exporter = OBJConverter._linkRIBExporter()

        # hack needed to instantiate scene
        self._dummy = TargetCamera( pos = (3,2,2), target = (0,0,0))

    def convert(self, src, dest):
        self._importFile(src)
        self._exportFile(dest)
        del self._reader
        del self._exporter
        del self._dummy

    def _importFile(self, filein):
        self._reader.importFile(filein)

    def _exportFile(self, dest):
        self._exporter.exportFile(dest)

    @staticmethod
    def _linkRIBExporter():
        pm = PluginManager()

        moddir = path.dirname(path.abspath(__file__))
        mod = path.join(moddir, 'crender_ribexporter.py')
        pdesc = pm.importPlugin(mod)

        objdesc = pm.findObject('crender_ribexporter.CRenderRIBExporter')
        cls = objdesc.object
        return cls()
