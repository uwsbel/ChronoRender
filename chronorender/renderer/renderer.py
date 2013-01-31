class RendererException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Renderer(object):
    STDOUT = 'stdout'
    RENDER = 'render'
    DETACH = 'detached'

    @staticmethod
    def getTypeName():
        return None

    def __init__(self):
        self._rendermodes = { Renderer.STDOUT : None, 
                Renderer.RENDER : None, Renderer.DETACH : None}
        self._rihook      = None
        self._libname     = None

    def __getattr__(self, name):
        # want to export rib's symbols as though they are in 
        # the renderer's namespace
        if hasattr(self._rihook, name):
            return self._rihook.__dict__[name]
        elif hasattr(self, name):
            return self.name
        else:
            raise AttributeError("render does not have symbol", name)

    def getRI(self):
        return self._rihook

    def getShaderCompiler(self):
        raise RendererException('no shader compiler for renderer')

    def getTextureProgram(self):
        raise RendererException('no texture program for renderer')

    def getBrickMapProgram(self):
        raise RendererException('no brickmap program for renderer')

    def isSupported(self, functionality):
        return True

    def init(self):
        return

    def cleanup(self):
        return

    def startRenderContext(self, mode=None):
        if not mode:
            self._rihook.Begin(self._rendermodes[Renderer.RENDER])
            return

        if mode in self._rendermodes:
            self._rihook.Begin(self._rendermodes[mode])
        else:
            self._rihook.Begin(mode)

    def stopRenderContext(self):
        self._rihook.End()
