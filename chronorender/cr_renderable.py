from cr_object import Object, ObjectException

# extended object, can be rendered
class RenderableException(ObjectException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Renderable(Object):
    _instanceid = 0

    def __init__(self, factories=None, *args, **kwargs):
        super(Renderable,self).__init__(factories=factories, *args, **kwargs)

        self._resolvedAssetPaths    = False
        self.instanced              = False
        self.instanceid             = Renderable._instanceid
        self.attributes             = []

        Renderable._instanceid += 1

    def __str__(self):
        return super(Renderable,self).__str__()

    def getInstanceID(self):
        return self.instanceid

    def getInstanceables(self):
        return []

    def resolveAssets(self, searchpaths):
        self._resolvedAssetPaths = True
        return  []

    def setAsset(self, assetname, obj):
        return

    def render(self, ri, *args, **kwargs):
        return

    def renderShape(self, rib, rendershaders=True, **kwargs):
        return


