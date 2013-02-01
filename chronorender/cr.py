import inspect, os

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
    
    _builtinClasses = [dp.SelectNode,
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
            ChronoRender._baseClasses, ChronoRender._builtinClasses,
            self._findDefaultConfigFile())

    def _findDefaultConfigFile(self):
        self._configpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return os.path.join(self._configpath, ChronoRender._defaultConfigFile)

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
