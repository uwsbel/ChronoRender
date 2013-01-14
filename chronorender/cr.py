
import plugin_manager as pm
import factory
import rndr_job as rndrjob

from geometry import Geometry
from renderobject import RenderObject
from renderpass import RenderPass
from rendersettings import RenderSettings
from shader import Shader

# create all singleton stuff
class ChronoRender():
    def __init__(self):
        self._plugins           = pm.PluginManager()
        self._factories         = {}
        self._jobs              = []

        self._initPlugins()
        self._initFactories()

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        self._createFactory(Geometry.getTypeName())
        self._createFactory(RenderObject.getTypeName())
        self._createFactory(RenderPass.getTypeName())
        self._createFactory(RenderSettings.getTypeName())
        self._createFactory(Shader.getTypeName())

    def _createFactory(self, typename):
        self._factories[typename] = factory.Factory(typename)
        modules = self._plugins.getPlugins(factory.Factory.getTypeName(), typename)
        self._factories[typename].setModules(modules)

    def createRenderJob(self, inxml):
        job = rndrjob.RndrJob(inxml, self._factories)
