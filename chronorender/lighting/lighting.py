from cr_object import Movable
from cr_scriptable import Scriptable
import chronorender.shader as cs

class Lighting(Movable):
    @staticmethod
    def getTypeName():
        return "lighting"

    def __init__(self, *args, **kwargs):
        super(Lighting,self).__init__(*args, **kwargs)
        self.archive    = self.getMember('filename')
        self.shaders    = self.getMember(cs.Shader.getTypeName())
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(Lighting, self)._initMembersDict()
        self._members['filename']                   = [str, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]
        self._members[cs.Shader.getTypeName()] = [cs.Shader, []]

    def resolveAssets(self, finder):
        out = []
        for shdr in self.shaders:
            out.extend(shdr.resolveAssets(finder))
        if self.script:
            out.extend(self.script.resolveAssets(finder))
        self._resolvedAssetPaths = True
        return out

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)
        elif self.archive != '':
            rib.RiReadArchive(self.archive)
        else:
            for shdr in self.shaders: 
                shdr.render(rib, **kwargs)

def build(**kwargs):
    return Lighting(**kwargs)
