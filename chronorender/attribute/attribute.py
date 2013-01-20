from cr_object import Object
               
class Attribute(Object):
    @staticmethod
    def getTypeName():
        return "attribute"

    def __init__(self, *args, **kwargs):
        super(Attribute,self).__init__(*args, **kwargs)
        self._name = self.getMember('name')

    def _initMembersDict(self):
        super(Attribute, self)._initMembersDict()
        self._members['name']   = [str, '']

    def render(self, rib):
        rib.RiAttribute(self._name, **self._params)

def build(**kwargs):
    return Attribute(**kwargs)
