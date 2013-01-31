from renderer import Renderer
import chronorender.ri as cri

class Aqsis(Renderer):
    @staticmethod
    def getTypeName():
        return 'aqsis'
    
    def __init__(self):
        super(Aqsis, self).__init__()
        self._libname = cri.rmanlibutil.libFromRenderer(Aqsis.getTypeName())

    def init(self):
        self._rihook = cri.loadRI(self._libname)
        self._initRenderModes()

    def cleanup(self):
        del self._rihook

    def _initRenderModes(self):
        # TODO NOT GOING TO STDOUT
        self._rendermodes[Renderer.STDOUT] = cri.RI_NULL
        self._rendermodes[Renderer.RENDER] = cri.RI_NULL
        self._rendermodes[Renderer.DETACH] = cri.RI_NULL

    def getShaderCompiler(self):
        return "aqsl"

    def getTextureProgram(self):
        return "teqsl"
