from chronorender.cr_object import Object
               
class Option(Object):
    @staticmethod
    def getTypeName():
        return "option"

    def getBaseName(self):
        return Option.getTypeName()

    def __init__(self, name=None, *args, **kwargs):
        super(Option,self).__init__(*args, **kwargs)
        self._name = name if name != None else self.getMember('name')

    def _initMembersDict(self):
        super(Option, self)._initMembersDict()
        self._members['name']   = [str, '']

    def updateMembers(self):
        super(Option, self).updateMembers()
        self.setMember('name', self._name)

    def render(self, rib):
        rib.Option(self._name, self._params)

def build(**kwargs):
    return Option(**kwargs)
