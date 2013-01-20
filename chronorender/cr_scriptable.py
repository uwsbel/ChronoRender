from cr_renderable import Renderable
import imp, sys, os

class ScriptableException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Scriptable(Renderable):
    @staticmethod
    def getTypeName():
        return "script"

    @staticmethod
    def _exportDirToSysPath(path):
        if path not in sys.path:
            sys.path.insert(0,path)

    def __init__(self, *args, **kwargs):
        super(Scriptable,self).__init__(*args, **kwargs)

        self.scriptname = self.getMember('file')
        self.funcname   = self.getMember('function')
        self.scriptpath = ""
        self._modname   = ""
        self._mod       = None
        self._func      = None

    def _initMembersDict(self):
        super(Scriptable,self)._initMembersDict()
        self._members['file']     = [str, '']
        self._members['function']   = [str, '']

    def resolveAssets(self, finder):
        self.scriptpath = finder.find(self.scriptname)
        self.scriptname = os.path.split(self.scriptpath)[1]

        self._verifyScriptName()
        # Scriptable._exportDirToSysPath(self.scriptpath)

        self._modname = os.path.splitext(self.scriptname)[0]
        self._resolvedAssetPaths = True

        # initialize with a test
        self._loadFunction(self._loadModule())

        return [self.scriptpath]

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, *args, **kwargs):
        func = self._loadFunction(self._loadModule())
        if func:
            func(rib, *args, **kwargs)
        # if self._func:
            # self._func(rib, *args, **kwargs)

    def _verifyScriptName(self):
        # if Scriptable.getTypeName() not in self.scriptname:
            # msg = 'words \"' + Scriptable.getTypeName() + '\" not in script filename'
            # raise ScriptableException(msg)
        return

    def _loadModule(self):
        try:
            return sys.modules[self._modname]
        except KeyError:
            pass

        try:
            # self._mod = imp.load_source(self._modname, self.scriptpath)
            return imp.load_source(self._modname, self.scriptpath)
        except ImportError as error:
            print error
            raise ScriptableException('could not load module: ' + self._modname)
            return none

    def _loadFunction(self, mod):
        # if not hasattr(self._mod, self.funcname):
        if not hasattr(mod, self.funcname):
            raise ScriptableException('function \"' + self.funcname + '\" not found in script: ' + self.scriptpath)

        # self._func = getattr(self._mod, self.funcname)
        return getattr(mod, self.funcname)

def build(**kwargs):
    return Scriptable(**kwargs)
