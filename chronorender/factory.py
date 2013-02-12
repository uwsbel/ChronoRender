import inspect, sys

class Factory():
    @staticmethod
    def getTypeName():
        return "factory"

    def __init__(self, objtype):
        self._classes               = []
        self._objectconstructors    = {}
        self._modules               = []
        self._objtype               = objtype

    def _loadObjects(self):
        for mod in self._modules:
            clsmembers = inspect.getmembers(sys.modules[mod.__name__], inspect.isclass)
            modclasses = []
            for cls in clsmembers:
                if cls[1].__module__ == mod.__name__:
                    modclasses.append(cls[1])

            for cls in modclasses:
                if hasattr(cls, 'getTypeName'):
                    if cls not in self._classes:
                        self._classes.append(cls)
                    self._objectconstructors[cls.getTypeName()] = mod.build


    def _clearObjects(self):
        self._objectconstructors.clear()

    def getFactoryType(self):
        return self._objtype

    def getClasses(self):
        return self._classes

    def getModules(self):
        return self._modules

    def setModules(self, modules):
        if isinstance(modules, list):
            self._modules += modules
        else:
            self._modules.append(modules)

        self._clearObjects()
        self._loadObjects()

    def addModule(self, module):
        self._modules.append(module)
        self._clearObjects()
        self._loadObjects()

    def removeModule(self, module):
        if module in self._modules:
            self._modules.remove(module)

    def build(self, typename, **kwargs):
        if typename not in self._objectconstructors:
            raise Exception('no object ' + str(typename) + ' for factory type ' + self.getFactoryType())

        return self._objectconstructors[typename](**kwargs)
