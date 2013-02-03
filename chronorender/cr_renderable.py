from chronorender.cr_object import Object, ObjectException
from chronorender.attribute import Attribute
from chronorender.option    import Option

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
        self.options                = self.getMember(Option.getTypeName())

        Renderable._instanceid += 1

    def _initMembersDict(self):
        super(Renderable, self)._initMembersDict()
        self._members[Attribute.getTypeName()]   = [Attribute, []]
        self._members[Option.getTypeName()]      = [Option, []]

    def getInstanceID(self):
        return self.instanceid

    def getInstanceables(self):
        return []

    def render(self, rib, *args, **kwargs):
        self.renderAttributes(rib)

    def renderAttributes(self, rib):
        for attr in self.attributes:
            attr.render(rib)

    def renderOptions(self, rib):
        for opt in self.options:
            opt.render(rib)

    def renderShape(self, rib, rendershaders=True, **kwargs):
        return

    def addAttribute(self, name, paramsdict):
        attr = Attribute(name)
        for key, val in paramsdict.iteritems():
          attr.addParameter(key, val)
        self.attributes.append(attr)

    def addOption(self, name, paramsdict):
        opt = Option(name)
        for key, val in paramsdict.iteritems():
          opt.addParameter(key, val)
        self.options.append(opt)
