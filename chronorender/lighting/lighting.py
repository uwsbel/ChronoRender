from chronorender.cr_renderable import Renderable
from chronorender.cr_scriptable import Scriptable
from chronorender.shader import Shader
               
class Lighting(Renderable):
    @staticmethod
    def getTypeName():
        return "lighting"

    def getBaseName(self):
        return Lighting.getTypeName()

    def __init__(self, *args, **kwargs):
        super(Lighting,self).__init__(*args, **kwargs)
        self.filename   = self.getMember('filename')
        self.shaders    = self.getMember(Shader.getTypeName())
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Lighting, self)._initMembersDict()
        self._members['filename']                 = [str, '']
        self._members[Scriptable.getTypeName()]   = [Scriptable, None]
        self._members[Shader.getTypeName()]       = [Shader, []]

    def updateMembers(self):
        super(Lighting, self).updateMembers()
        self.setMember('filename', self.filename)
        self.setMember(Scriptable.getTypeName(), self.script)
        self.setMember(Shader.getTypeName(), self.shaders)

    def resolveAssets(self, assetman):
        out = []
        for shdr in self.shaders:
            out.extend(shdr.resolveAssets(assetman))

        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        elif self.filename != '':
            # self.filename = finder.find(self.filename)
            out.append(assetman.find(self.filename))

        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        elif self.filename != '':
            rib.ReadArchive(self.filename)
        else:
            for shdr in self.shaders: 
                shdr.render(rib, **kwargs)

def build(**kwargs):
    return Lighting(**kwargs)
