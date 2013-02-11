from cr_renderable import Renderable
import imp, sys, os

class Scriptable(Renderable):
    @staticmethod
    def getTypeName():
        return "script"

    def getBaseName(self):
        return Renderable.getTypeName()

    @staticmethod
    def _exportDirToSysPath(path):
        if path not in sys.path:
            sys.path.insert(0,path)

    def __init__(self, *args, **kwargs):
        super(Scriptable,self).__init__(*args, **kwargs)

        self.scriptname = self.getVar('scriptname', kwargs)
        self.function   = self.getVar('function', kwargs)
        self.scriptpath = ""
        self._modname   = ""
        self._mod       = None
        self._func      = None

        self._parseModInformation()

    def _initMembersDict(self):
        super(Scriptable,self)._initMembersDict()
        self._members['scriptname']     = [str, '']
        self._members['function']   = [str, '']

    def updateMembers(self):
        super(Scriptable, self).updateMembers()
        self.setMember('scriptname', self.scriptname)
        self.setMember('function', self.function)

    def resolveAssets(self, assetman):
        try:
            self.scriptpath = assetman.find(self.scriptname)
        except Exception:
            pass
        self._parseModInformation()
        self._resolvedAssetPaths = True

        return [self.scriptpath]

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, *args, **kwargs):
        func = self._loadFunction(self._loadModule())
        if func:
            func(rib, *args, **kwargs)

    def _parseModInformation(self):
        self._modname = os.path.splitext(self.scriptname)[0]

    def _loadModule(self):
        try:
            return sys.modules[self._modname]
        except KeyError:
            pass

        try:
            return imp.load_source(self._modname, self.scriptpath)
        except ImportError as error:
            print error
            raise ImportError('could not load module: ' + self._modname)
            return none

    def _loadFunction(self, mod):
        if not hasattr(mod, self.function):
            raise ImportError('function \"' + self.function + '\" not found in script: ' + self.scriptpath)

        return getattr(mod, self.function)

def build(**kwargs):
    return Scriptable(**kwargs)
