import os

from chronorender.cr_renderable import Renderable, RenderableException
from chronorender.finder import FinderFactory
import chronorender.rsl as rsl

class ShaderException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Shader(Renderable):

    @staticmethod
    def getTypeName():
        return "shader"

    def getBaseName(self):
        return Shader.getTypeName()

    def __init__(self, shdrpath='', *args, **kwargs):
        super(Shader,self).__init__(*args, **kwargs)

        self._shdrparams = []
        self._paramdict = {}
        self._firstshdr = None
        self._filename  = self.getMember('name')

        if shdrpath != '':
            self._initFromFullPath(shdrpath)

    def _initFromFullPath(self, shdrpath):
            if not os.path.isfile(shdrpath):
                raise ShaderException(shdrpath + " is not a shader file")
            path, self._filename = os.path.split(shdrpath)
            self.resolveAssets(FinderFactory.build([path]))

    def _initMembersDict(self):
        super(Shader, self)._initMembersDict()

        self._members['name'] = [str, '']

    def updateMembers(self):
        super(Shader, self).updateMembers()

    def _initShaderParameters(self):
        self._parseShaderParameters()
        self._convertDefaultsToPythonTypes()
        self._initFirstShader()   
        self._constructParameterDict()

    def _parseShaderParameters(self):
        self._shdrparams = rsl.slparams(self._shdrpath)
        if len(self._shdrparams) <= 0:
            raise ShaderException('no shaders in source file: ' +
                    self.getMember('name'))

    def _convertDefaultsToPythonTypes(self):
        for shader in self._shdrparams:
            for param in shader.params:
                param.default = rsl.convertdefault(param)

    def _initFirstShader(self):
        self._firstshdr = self._shdrparams[0]

    def _constructParameterDict(self):
        for param in self._firstshdr.params:
            val = param.default
            
            try:
                tmp = self.getMember(param.name)
                val = type(param.default)(tmp)
            except Exception:
                val = param.default

            self._paramdict[param.name] = val

    def _getDeclParameterDict(self):
        d = {}
        for param in self._firstshdr.params:
            val = self._paramdict[param.name]
            d[param.type + ' ' + param.name] = val
        return d

    def getShaderType(self):
        return self._firstshdr.type

    def getShaderName(self):
        return self._firstshdr.name

    def getParameters(self):
        return self._paramdict

    def resolveAssets(self, assetman):
        if self._filename:
            self._shdrpath = assetman.find(self._filename)
            self._initShaderParameters()
            self._resolvedAssetPaths = True
            return [self._shdrpath]
        return []

    def setAsset(self, assetname, obj):
        if assetname in self._paramdict:
            vtype = type(self._paramdict[assetname])
            self._paramdict[assetname] = vtype(obj)

    def render(self, rib, *args, **kwargs):
        if not self._filename: return
        stype = self.getShaderType()
        rdict = self._getDeclParameterDict()
        if stype == 'surface':
            rib.Surface(self.getShaderName(), rdict)
        elif stype == 'displacement':
            rib.Displacement(self.getShaderName(), rdict)
        elif stype == 'volume':
            rib.Volume(self.getShaderName(), rdict)
        elif stype == 'light':
            rib.LightSource(self.getShaderName(), rdict)
        elif stype == 'imager':
            rib.Imager(self.getShaderName(), rdict)

def build(**kwargs):
    return Shader(**kwargs)
