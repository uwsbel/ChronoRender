import os

from renderer import Renderer
import chronorender.ri as ri
from chronorender.cr_utils import findModuleOnSysPath

class PRMan(Renderer):
    _rmantree = os.environ['RMANTREE']

    @staticmethod
    def getName():
        return 'prman'
    
    def __init__(self):
        super(PRMan, self).__init__()
        self._libname = ri.rmanlibutil.libFromRenderer(PRMan.getName())
        self._modname = None
        self._module  = None
        self._dir     = None

    def __getattr__(self, name):
        # want to export rib's symbols as though they are in 
        # the renderer's namespace
        if name in self._dir:
            return self._dir[name]
        elif hasattr(self, name):
            return self.name
        else:
            raise AttributeError("render does not have symbol", name)

    def init(self):
        self._loadPRManForPython()
        self._initRenderModes()

    def cleanup(self):
        del self._rihook

    def _initRenderModes(self):
        self._rendermodes[Renderer.STDOUT] = ri.RI_NULL
        self._rendermodes[Renderer.RENDER] = ri.RI_RENDER
        self._rendermodes[Renderer.DETACH] = "launch:prman? -ctrl $ctrlin \
                $ctrlout -dspy $dspyin $dspyout -xcpt $xcptin"

    def getShaderCompiler(self):
        return "shader"

    def getTextureProgram(self):
        return "texmake"

    def getBrickMapProgram(self):
        return "brickmake"

    def _loadPRManForPython(self):
        self._findPRManForPython()
        self._importPRManForPython()
        self._createRIHookFromModule()

    def _findPRManForPython(self):
        mod = findModuleOnSysPath('prman.py', PRMan._rmantree)
        if not mod:
          raise RendererException, 'could not find prman Python interface'
        self._modname = mod

    def _importPRManForPython(self):
        try:
            self._module = __import__(self._modname)
        finally:
            pass
        
    def _createRIHookFromModule(self):
        if not hasattr(self._module, 'Ri'):
            raise RendererException, 'invalid PRman Python interface, no Ri symbol'
        self._rihook = self._module.Ri()
        self._dir = dict((name, getattr(self._rihook, name)) for name in dir(self._rihook) if not name.startswith('__'))
