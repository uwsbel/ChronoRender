from renderer import Renderer
import chronorender.ri as cri

class Stdout(Renderer):
    @staticmethod
    def getTypeName():
        return 'stdout'
    
    def __init__(self):
        super(Stdout, self).__init__()
        self._libname = None

    def init(self):
        self._rihook = cri.ri_noprefix
        #self._rihook = cri.ri
        self._initRenderModes()

    def _initRenderModes(self):
        self._rendermodes[Renderer.STDOUT] = cri.RI_NULL
        self._rendermodes[Renderer.RENDER] = cri.RI_NULL
        self._rendermodes[Renderer.DETACH] = cri.RI_NULL
