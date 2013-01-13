
import meta_data as md
import plugin_manager as pm
import geometry_factory as gf

class ChronoRender():
    def __init__(self):
        self._metadata = md.MetaData()
        self._plugins = pm.PluginManager()
        self._geofactory = gf.GeometryFactory()

        self._initPlugins()
        self._initFactories()

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        modules = self._plugins.getPlugins(self._geofactory.getTypeName(),
                self._geofactory.getFactoryType())
        self._geofactory.setModules(modules)

    def createRenderJob(self, inxml):
        return
