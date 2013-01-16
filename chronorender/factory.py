from cr_object import Object

class Factory(Object):
    @staticmethod
    def getTypeName():
        return "factory"

    def __init__(self, objtype):
        super(Factory,self).__init__()

        self._objectconstructors = {}
        self._modules = []
        self._objtype = objtype

    def _loadObjects(self):
        self._objectconstructors.clear()
        for mod in self._modules:
            obj = mod.build()
            self._objectconstructors[obj.getTypeName()] = mod.build

    def getFactoryType(self):
        return self._objtype

    def setModules(self, modules):
        self._modules = modules
        self._loadObjects()

    def build(self, typename, **kwargs):
        if typename not in self._objectconstructors:
            raise Exception('no object ' + typename + ' for factory type ' +
                    self.getFactoryType())

        return self._objectconstructors[typename](**kwargs)

    def __str__(self):
        return str(self._objectconstructors)
