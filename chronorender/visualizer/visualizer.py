from cr_object import Renderable
from cr_scriptable import Scriptable

class Visualizer(Renderable):
    @staticmethod
    def getTypeName():
        return "visualizer"

    def __init__(self, *args, **kwargs):
        super(Visualizer,self).__init__(*args, **kwargs)
        self.script     = self.getMember(Scriptable.getTypeName())
        return

    def _initMembersDict(self):
        super(Visualizer, self)._initMembersDict()
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def render(self, rib, *args, **kwargs):
        if self.script:
            self.script.render(rib, *args, **kwargs)

def build(**kwargs):
    return Visualizer(**kwargs)
