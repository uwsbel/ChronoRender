
import meta_data as md
import plugin_manager as pm
import factory

class ChronoRender():
    def __init__(self):
        self._metadata = md.MetaData()
        self._plugins = pm.PluginManager()
        self._geofactory = factory.Factory('geometry')

        self._initPlugins()
        self._initFactories()

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        modules = self._plugins.getPlugins(self._geofactory.getTypeName(),
                self._geofactory.getFactoryType())
        self._geofactory.setModules(modules)
        sph = self._geofactory.build({'name' : 'sphere'})
        cube = self._geofactory.build({'name' : 'cube'})

    def createRenderJob(self, inxml):
        return
