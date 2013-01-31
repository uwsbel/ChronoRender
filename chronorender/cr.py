import inspect, os, shutil
import thirdparty.yaml as yaml

import chronorender.plugins as pm
import chronorender.factory as factory
import chronorender.rndr_job as rndrjob
import chronorender.factorydict as fdict
import chronorender.cr_object as cr_object
import chronorender.cr_utils as cr_utils

import chronorender.attribute as attr
import chronorender.dataprocess as dp
import chronorender.datasource as ds
import chronorender.distributed as distrib
import chronorender.geometry as geo
import chronorender.movie as mov
import chronorender.renderpass as rp

import chronorender.camera as cam
import chronorender.data as data
import chronorender.lighting as lighting
import chronorender.renderobject as renderobject
import chronorender.rendersettings as rendersettings
import chronorender.scene as scene
import chronorender.simulation as simulation
import chronorender.shader as shader
import chronorender.visualizer as visualizer
import chronorender.cr_scriptable as scriptable

class ChronoRender(object):
    _defaultConfigFile = 'cr.conf.yml'
    _baseClasses = [attr.Attribute,
                    cam.Camera,
                    data.DataObject,
                    dp.DataProcess,
                    ds.DataSource,
                    geo.Geometry,
                    lighting.Lighting,
                    mov.Movie,
                    renderobject.RenderObject,
                    rp.RenderPass,
                    rp.settings.Settings,
                    rp.display.Display,
                    rendersettings.RenderSettings,
                    scene.Scene,
                    simulation.Simulation,
                    shader.Shader,
                    visualizer.Visualizer,
                    scriptable.Scriptable]

    def __init__(self):
        self._jobs              = []

        self._plugins           = pm.PluginManager()
        self._factories         = fdict.FactoryDict()

        self._processConfig()
        self._initPlugins()
        self._initFactories()


    def _processConfig(self):
        yam = self._readConfig()

        # distrib.JobDescriptor._queue = yam['distributed']['queue']
        # fact = distrib.DistributedFactory()
        # dist = fact.build()
        # job = dist.createJobTemplate()
        # print job.queue

    def _readConfig(self):
        f = open(self._findDefaultConfigFile())
        yam = yaml.safe_load(f)
        f.close()
        return yam

    def _findDefaultConfigFile(self):
        self._configpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return os.path.join(self._configpath, ChronoRender._defaultConfigFile)

    def _initPlugins(self):
        self._plugins.loadPlugins()
        self._plugins.registerPlugins()

    def _initFactories(self):
        self._initBaseClassFactories()
        self._initBuiltInClassFactories()

    def _initBaseClassFactories(self):
        for cls in ChronoRender._baseClasses:
            self._createFactory(cls)

    def _initBuiltInClassFactories(self):
        self._addFactoryModule(dp.DataProcess, dp.SelectNode)
        self._addFactoryModule(ds.DataSource, ds.CSVDataSource)
        self._addFactoryModule(geo.Geometry, geo.Sphere)
        self._addFactoryModule(geo.Geometry, geo.File)
        self._addFactoryModule(mov.Movie, mov.FFMPEG)
        self._addFactoryModule(rp.RenderPass, rp.RayTracePass)
        self._addFactoryModule(rp.RenderPass, rp.OcclusionPass)

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

    def createAndRunRenderJob(self, mdfile, stream='', framerange=None):
        job = self._createRenderJob(mdfile)
        job.stream = stream

        try:
            job.run(framerange)
        except Exception as e:
            print e
        finally:
            exit()

    def createAndSubmitRenderJob(self, mdfile, stream=''):
        job = self._createRenderJob(mdfile)
        self._submitRenderJob(job)

    def _createRenderJob(self, mdfile):
        return rndrjob.RndrJob(mdfile, self._factories)

    def _submitRenderJob(self, job):
        return
