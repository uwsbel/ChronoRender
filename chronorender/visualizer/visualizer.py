from cr_object import Renderable

class Visualizer(Renderable):
    @staticmethod
    def getTypeName():
        return "visualizer"

    def __init__(self):
        return

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

def build(**kwargs):
    return Visualizer(**kwargs)
