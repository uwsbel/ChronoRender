
import plugin_manager as pm
import factory
import rndr_job as rndrjob

from datareader import DataReader
from geometry import Geometry
from lighting import Lighting
from renderobject import RenderObject
from renderpass import RenderPass
from rendersettings import RenderSettings
from scene import Scene
from simulation import Simulation
from shader import Shader
from visualizer import Visualizer

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
        self._createFactory(DataReader.getTypeName())
        self._createFactory(Geometry.getTypeName())
        self._createFactory(Lighting.getTypeName())
        self._createFactory(RenderObject.getTypeName())
        self._createFactory(RenderPass.getTypeName())
        self._createFactory(RenderSettings.getTypeName())
        self._createFactory(Scene.getTypeName())
        self._createFactory(Simulation.getTypeName())
        self._createFactory(Shader.getTypeName())
        self._createFactory(Visualizer.getTypeName())
        print self._factories

    def _createFactory(self, typename):
        self._factories[typename] = factory.Factory(typename)
        modules = self._plugins.getPlugins(factory.Factory.getTypeName(), typename)
        self._factories[typename].setModules(modules)

    def createAndRunRenderJob(self, inxml):
        job = self._createRenderJob(inxml)
        job.run()

    def createAndSubmitRenderJob(self, inxml):
        job = self._createRenderJob(inxml)
        self._submitRenderJob(job)

    def _createRenderJob(self, inxml):
        return rndrjob.RndrJob(inxml, self._factories)

    def _submitRenderJob(self, job):
        return
