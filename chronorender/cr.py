import inspect, os, shutil

import chronorender.plugins as pm
import chronorender.factory as factory
import chronorender.rndr_job as rndrjob
import chronorender.factorydict as fdict
import chronorender.cr_object as cr_object
import chronorender.dataprocess as dp
import chronorender.datasource as ds
import chronorender.geometry as geo
import chronorender.renderpass as rp
import chronorender.attribute as attr
import chronorender.cr_utils as cr_utils

from chronorender.camera import Camera
from chronorender.data import DataObject
from chronorender.lighting import Lighting
from chronorender.renderobject import RenderObject
from chronorender.rendersettings import RenderSettings
from chronorender.scene import Scene
from chronorender.simulation import Simulation
from chronorender.shader import Shader
from chronorender.visualizer import Visualizer
from cr_scriptable import Scriptable

class ChronoRender():
    def __init__(self, plugins=True):
        self._jobs              = []

        if  plugins:
            self._plugins           = pm.PluginManager()
            self._factories         = fdict.FactoryDict()

            self._initPlugins()
            self._initFactories()

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        self._createFactory(attr.Attribute)

        self._createFactory(Camera)

        self._createFactory(DataObject)

        self._createFactory(dp.DataProcess)
        self._addFactoryModule(dp.DataProcess, dp.SelectNode)

        self._createFactory(ds.DataSource)
        self._addFactoryModule(ds.DataSource, ds.CSVDataSource)

        self._createFactory(geo.Geometry)
        self._addFactoryModule(geo.Geometry, geo.Sphere)
        self._addFactoryModule(geo.Geometry, geo.File)

        self._createFactory(Lighting)
        self._createFactory(RenderObject)

        self._createFactory(rp.RenderPass)
        self._addFactoryModule(rp.RenderPass, rp.RayTracePass)
        self._createFactory(rp.settings.Settings)
        self._createFactory(rp.display.Display)

        self._createFactory(RenderSettings)
        self._createFactory(Scene)
        self._createFactory(Scriptable)
        self._createFactory(Simulation)
        self._createFactory(Shader)
        self._createFactory(Visualizer)

    def _createFactory(self, cls):
        modules = self._plugins.getPlugins(factory.Factory.getTypeName(), cls.getTypeName())
        # add default constructor
        modules.append(inspect.getmodule(cls))
        self._factories.addFactory(cls.getTypeName(), modules)

    def _addFactoryModule(self, basecls, cls):
        self._factories.appendFactory(basecls.getTypeName(), inspect.getmodule(cls))

    def getFactories(self, typename):
        return self._factories.getFactory(typename)

    def generateRenderJobToDisk(self, dest):
        defaultmd = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default.yml')
        job = self._createRenderJob(defaultmd)

        outpath = os.path.join(dest, "RENDERMAN")

        job.setOutputPath(outpath)
        job.createOutDirs()

        defaultscene = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_scene.rib')
        defaultcam = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_camera.rib')
        defaultlighting = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_lighting.rib')
        job.copyAssetToDirectory(defaultscene)
        job.copyAssetToDirectory(defaultcam)
        job.copyAssetToDirectory(defaultlighting)
        shutil.copy2(defaultmd, outpath)

    def updateJobAssets(self, mdfile):
        job = self._createRenderJob(mdfile)
        dest = os.path.abspath(os.path.split(mdfile)[0])

        job.setOutputPath(dest)
        job.updateAssets()

    def createAndRunRenderJob(self, mdfile, stream=''):
        job = self._createRenderJob(mdfile)
        job.run(stream)

    def createAndSubmitRenderJob(self, mdfile):
        job = self._createRenderJob(mdfile)
        self._submitRenderJob(job)

    def _createRenderJob(self, mdfile):
        return rndrjob.RndrJob(mdfile, self._factories)

    def _submitRenderJob(self, job):
        return
