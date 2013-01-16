from factory import Factory

class FactoryDict():
    def __init__(self):
        self._factories = {}

    def __str__(self):
        return str(self._factories)

    def addFactory(self, typename, modules):
        self._factories[typename] = Factory(typename)
        self._factories[typename].setModules(modules)

    def getFactory(self, typename):
        try:
            return self._factories[typename]
        except KeyError as ke:
            print ke
            return None

    def buildObject(self, cls, instances):
        out = None
        if isinstance(instances, list):
            out = []
            for inst in instances:
                out.append(self._buildObject(cls, inst))
        else:
            out = self._buildObject(cls, instances)
        return out

    def _buildObject(self, cls, instance):
        qual = cls.getInstanceQualifier()
        if qual not in instance:
            instance[qual] = cls.getTypeName()
        concrete_name = instance[qual]
        return self._factories[cls.getTypeName()].build(concrete_name, **instance)
