import inspect, os, shutil
from chronorender.thirdparty import resource_filename

import chronorender.rndr_job as rndrjob
import chronorender.cr_object as cr_object
import chronorender.cr_utils as cr_utils
import chronorender.cr_constructor as cr_constructor

import chronorender.attribute as attr
import chronorender.camera as cam
import chronorender.data as data
import chronorender.dataprocess as dp
import chronorender.datasource as ds
import chronorender.distributed as distrib
import chronorender.geometry as geo
import chronorender.lighting as lighting
import chronorender.movie as mov
import chronorender.renderobject as renderobject
import chronorender.renderpass as rp
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
                    distrib.Distributed,
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


    _pluginClasses = [attr.Attribute,
                    cam.Camera,
                    data.DataObject,
                    dp.DataProcess,
                    ds.DataSource,
                    distrib.Distributed,
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
                    
    
    _builtinPlugins = [dp.SelectNode,
                      ds.CSVDataSource,
                      geo.Sphere,
                      geo.File,
                      mov.FFMPEG,
                      rp.RayTracePass,
                      rp.OcclusionPass]

    def __init__(self):
        self._jobs              = []
        self._constructor       = cr_constructor.CRConstructor()
        self._factories         = self._constructFactories()

    def _constructFactories(self):
        return self._constructor.buildAndConfigureFactories(
            ChronoRender._baseClasses, ChronoRender._builtinPlugins,
            self._findDefaultConfigFile())

    def _findDefaultConfigFile(self):
        # self._configpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # return os.path.join(self._configpath, ChronoRender._defaultConfigFile)
        self._configpath = os.path.dirname(resource_filename(__name__,
            ChronoRender._defaultConfigFile))
        return os.path.join(self._configpath, ChronoRender._defaultConfigFile)

    def getFactories(self, typename=None):
        if not typename:
            return self._factories
        else:
            return self._factories.getFactory(typename)

    def writeJobToDisk(self, job, dest):
        outpath = os.path.join(dest, "RENDERMAN")
        job.setOutputPath(outpath)
        job.createOutDirs()
        self._writeDefaultAssets()
        self._copyJobMetaDataToPath(job, outpath)

    def createJob(self, mdfile=None)#, stream=None):
        if not mdfile:
            mdfile = self._getDefaultMetaData()
        return rndrjob.RndrJob(mdfile,  self._factories)

    def updateJobAssets(self, job):
        mdfile = job.getMetaData().filename
        dest = os.path.abspath(os.path.split(mdfile)[0])

        job.setOutputPath(dest)
        job.updateAssets()

    def runJob(self, job):
        job.run()

    def submitJob(self, job, prog):
        try:
            job.submit(prog)
        except Exception as e:
            print e
        finally:
            pass

    def runRenderJob(self, job):
        try:
            job.run()
        except Exception as e:
            print e
        finally:
            pass

    def _getDefaultMetaData(self):
        return cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default.yml')

    def _writeDefaultAssets(self):
        # import pdb; pdb.set_trace()
        defaultscene = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_scene.rib')
        job.copyAssetToDirectory(defaultscene)
        defaultcam = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_camera.rib')
        job.copyAssetToDirectory(defaultcam)
        defaultlighting = cr_utils.getAbsPathRelativeToModule(ChronoRender, './assets/default_lighting.rib')
        job.copyAssetToDirectory(defaultlighting)
        defaultshader = cr_utils.getAbsPathRelativeToModule(ChronoRender, '.assets/matte.sl')
        job.copyAssetToDirectory(defaultshader)
        ao = cr_utils.getAbsPathRelativeToModule(ChronoRender, '.assets/occlusionsurf.sl')
        job.copyAssetToDirectory(ao)
        colorbleeding = cr_utils.getAbsPathRelativeToModule(ChronoRender, '.assets/colorbleedinglight.sl')

    def _copyJobMetaDataToPath(self, job, oupath):
        shutil.copy2(job.getMetaData().filename, outpath)

