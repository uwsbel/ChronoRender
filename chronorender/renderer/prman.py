from renderer import Renderer
import chronorender.ri as ri

class PRMan(Renderer):
    @staticmethod
    def getName():
        return 'prman'
    
    def __init__(self):
        super(PRMan, self).__init__()
        self._libname = ri.rmanlibutil.libFromRenderer(PRMan.getName())

    def init(self):
        self._rihook = ri.loadRI(self._libname)
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
