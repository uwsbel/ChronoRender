from cr_object import Object, ObjectException
from attribute import Attribute

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
        self.attributes             = self.getMember(Attribute.getTypeName())

        Renderable._instanceid += 1

    def _initMembersDict(self):
        super(Renderable, self)._initMembersDict()
        self._members[Attribute.getTypeName()]   = [Attribute, []]

    def getInstanceID(self):
        return self.instanceid

    def getInstanceables(self):
        return []

    def resolveAssets(self, finder, outpath):
        self._resolvedAssetPaths = True
        return  []

    def setAsset(self, assetname, obj):
        return


    def render(self, rib, *args, **kwargs):
        self.renderAttributes(rib)

    def renderAttributes(self, rib):
        for attr in self.attributes:
            attr.render(rib)

    def renderShape(self, rib, rendershaders=True, **kwargs):
        return


