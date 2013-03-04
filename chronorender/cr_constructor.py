import inspect, os
import thirdparty.yaml as yaml
import chronorender.plugins as pm
import chronorender.factory as factory
import chronorender.factorydict as fdict

from pkg_resources import resource_string, resource_filename, resource_stream

class CRConstructor(object):
    def __init__(self):
        self._baseClassDict     = {}
        self._plugins           = pm.PluginManager()
        self._factories         = fdict.FactoryDict()

    def buildAndConfigureFactories(self, baseclasses, builtinclasses, configfile):
        self._initBaseClassesDict(baseclasses)
        self._processConfig(configfile)
        self._initPlugins()
        self._initFactories(builtinclasses)
        return self._factories

    def _initBaseClassesDict(self, baseclasses):
        self._baseClassDict = {}
        for cls in baseclasses:
            self._baseClassDict[cls.getTypeName()] = cls

    def _configureBaseClasses(self, config):
        for key, attrdict in config.iteritems():
            if key not in self._baseClassDict:
                continue
            cls = self._baseClassDict[key]
            self._configAttribute(cls, attrdict)

    def _configAttribute(self, cls, attr):
        if isinstance(attr, dict):
            for k, v in attr.iteritems():
                self._setClassAttribute(cls, k, v)

    def _setClassAttribute(self, cls, name, val):
        if hasattr(cls, name):
            setattr(cls, name, val)
        else:
            raise Exception, str(cls) +  " does not have attribute " + name

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self, builtins):
        self._initBaseClassFactories()
        self._initBuiltInClassFactories(builtins)

    def _initBaseClassFactories(self):
        for typename, cls in self._baseClassDict.iteritems():
            self._createFactory(cls)

    def _initBuiltInClassFactories(self, classes):
        for cls in classes:
            base = self._findBaseFactoryForClass(cls)
            if not base:
              raise Exception, "no base class for class: " + str(cls)
            self._addFactoryModule(base, cls)

    def _findBaseFactoryForClass(self, cls):
        bases = inspect.getmro(cls)
        for b in bases:
            if b.getTypeName() in self._baseClassDict:
                return b
        return None

    def _createFactory(self, cls):
        modules = self._plugins.getPlugins(factory.Factory.getTypeName(), cls.getTypeName())
        # add default constructor
        modules.append(inspect.getmodule(cls))
        self._factories.addFactory(cls.getTypeName(), modules)

    def _addFactoryModule(self, basecls, cls):
        self._factories.appendFactory(basecls.getTypeName(), inspect.getmodule(cls))

    def getFactoryDict(self):
        return self._factories

    def _processConfig(self, yml_file):
        yam = self._readConfig(yml_file)
        self._configureBaseClasses(yam)

    def _readConfig(self, yml_file):
        # f = open(yml_file)
        f = resource_stream(__name__, 'cr.conf.yml')
        yam = yaml.safe_load(f)
        f.close()
        return yam
