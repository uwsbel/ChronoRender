from cr_object import Renderable, RenderableException
import slparams
import os
import finder as mfind

class ShaderException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Shader(Renderable):

    @staticmethod
    def getTypeName():
        return "shader"

    def __init__(self, *args, **kwargs):
        super(Shader,self).__init__(*args, **kwargs)

        self._shdrparams = []
        self._paramdict = {}
        self._firstshdr = None
        self._shdrpath = ''

    def _initMembersDict(self):
        self._members['type']   = [str, 'Surface']
        self._members['name']   = [str, 'plastic.sl']

    def _initShaderParameters(self):
        self._parseShaderParameters()
        self._convertDefaultsToPythonTypes()
        self._initFirstShader()
        self._constructParameterDict()

    def _parseShaderParameters(self):
        if self._shdrpath == '': return

        self._shdrparams = slparams.slparams(self._shdrpath)
        if len(self._shdrparams) <= 0:
            raise ShaderException('no shaders in source file: ' +
                    self.getMember('name'))

    def _convertDefaultsToPythonTypes(self):
        for shader in self._shdrparams:
            for param in shader.params:
                param.default = slparams.convertdefault(param)

    def _initFirstShader(self):
        self._firstshdr = self._shdrparams[0]

    def _constructParameterDict(self):
        for param in self._firstshdr.params:
            val = param.default
            
            # check if parameterized
            try:
                tmp = self.getMember(param.name)
                val = type(param.default)(tmp)
            except Exception:
                val = param.default

            self._paramdict[param.name] = val

    def getInfo(self):
        return self._firstshdr

    def getParameters(self):
        return self._paramdict

    # methods of Renderable class
    def resolveAssets(self, finder):
        self._shdrpath = finder.find(self.getMember('name'))
        self._initShaderParameters()
        self._resolvedAssetPaths = True

    def render(self, *args, **kwargs):
        return

def build(**kwargs):
    return Shader(**kwargs)
