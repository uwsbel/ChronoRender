from cr_object import Object
import slparams
import os

class ShaderException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Shader(Object):

    def __init__(self, *args, **kwargs):
        super(Shader,self).__init__(*args, **kwargs)

        self._shdrparams = []
        self._paramdict = {}

        self._initShaderParameters()

    def _initMembersDict(self):
        self._members['type']   = [str, 'Surface']
        self._members['name']   = [str, 'plastic.sl']

    def _initShaderParameters(self):
        self._parseShaderParameters()
        self._convertDefaultsToPythonTypes()
        self._constructParameterDict()

    def _parseShaderParameters(self):
        self._shdrparams = slparams.slparams(self.getMember('name'))
        if len(self._shdrparams) <= 0:
            raise ShaderException('no shaders in source file: ' +
                    self.getMember('name'))

    def _convertDefaultsToPythonTypes(self):
        for shader in self._shdrparams:
            for param in shader.params:
                param.default = slparams.convertdefault(param)

    def _constructParameterDict(self):
        shader = self._shdrparams[0]
        for param in shader.params:
            val = param.default
            self._paramdict[param.name] = val

    def getParameters(self):
        return self._paramdict

    def getTypeName(self):
        return 'shader'
