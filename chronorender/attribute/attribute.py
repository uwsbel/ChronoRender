from chronorender.cr_object import Object
               
class Attribute(Object):
    @staticmethod
    def getTypeName():
        return "attribute"

    def __init__(self, name=None, *args, **kwargs):
        super(Attribute,self).__init__(*args, **kwargs)
        self._name = name if name != None else self.getMember('name')

    def _initMembersDict(self):
        super(Attribute, self)._initMembersDict()
        self._members['name']   = [str, '']

    def render(self, rib):
        # rib.Attribute(self._name, **self._params)
        rib.Attribute(self._name, self._params)

def build(**kwargs):
    return Attribute(**kwargs)
