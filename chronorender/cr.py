import inspect
import chronorender.plugins as pm
import factory
import rndr_job as rndrjob
import factorydict as fdict

from ribgenerator import RIBGenerator
from chronorender.data import DataObject
import chronorender.dataprocess as dp
import chronorender.datasource as ds
from chronorender.geometry import Geometry
from chronorender.lighting import Lighting
from chronorender.renderobject import RenderObject
from chronorender.renderpass import RenderPass
from chronorender.rendersettings import RenderSettings
from chronorender.scene import Scene
from chronorender.simulation import Simulation
from chronorender.shader import Shader
from chronorender.visualizer import Visualizer

# create all singleton stuff
class ChronoRender():
    def __init__(self):
        self._plugins           = pm.PluginManager()
        self._factories         = fdict.FactoryDict()
        self._jobs              = []

        self._initPlugins()
        self._initFactories()

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        self._createFactory(DataObject)
        self._createFactory(dp.DataProcess)
        self._addFactoryModule(dp.DataProcess, dp.SelectNode)
        self._createFactory(ds.DataSource)
        self._addFactoryModule(ds.DataSource, ds.CSVDataSource)
        self._createFactory(Geometry)
        self._createFactory(Lighting)
        self._createFactory(RenderObject)
        self._createFactory(RenderPass)
        self._createFactory(RenderSettings)
        self._createFactory(Scene)
        self._createFactory(Simulation)
        self._createFactory(Shader)
        self._createFactory(Visualizer)

    def _createFactory(self, cls):
        modules = self._plugins.getPlugins(factory.Factory.getTypeName(), cls.getTypeName())
        # add default constructor
        modules.append(inspect.getmodule(cls))
        self._factories.addFactory(cls.getTypeName(), modules)
        # print self.getFactories(cls.getTypeName())

    def _addFactoryModule(self, basecls, cls):
        self._factories.appendFactory(basecls.getTypeName(), inspect.getmodule(cls))

    def getFactories(self, typename):
        return self._factories.getFactory(typename)

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
