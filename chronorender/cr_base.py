import inspect, os, shutil
import chronorender.rndr_job as rndrjob
import chronorender.cr_object as cr_object
import chronorender.cr_utils as cr_utils
import chronorender.cr_constructor as cr_constructor

class ChronoRenderBase(object):
    _defaultConfigFile = 'cr.conf.yml'

    def __init__(self):
        self._baseClasses       = []
        self._pluginClasses     = []
        self._builtinPlugins    = []
        self._jobs              = []
        self._constructor       = cr_constructor.CRConstructor()
        self._factories         = self._constructFactories()

    def _constructFactories(self):
        return self._constructor.buildAndConfigureFactories(
            self._baseClasses, self._builtinPlugins,
            self._findDefaultConfigFile())

    def _findDefaultConfigFile(self):
        self._configpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        return os.path.join(self._configpath, ChronoRenderBase._defaultConfigFile)

    def getFactories(self, typename=None):
        if not typename:
            return self._factories
        else:
            return self._factories.getFactory(typename)

    def writeJobToDisk(self, job, dest=''):
        if dest == '':
            dest = os.path.join(os.getcwd(), "RENDERMAN")
        job.setOutputPath(dest)
        job.createOutDirs()
        self._writeDefaultAssets(job)
        self._copyJobMetaDataToPath(job, dest)

    def createJob(self, mdfile=None, frange=[0,0], renderer=None):
        if not mdfile:
            mdfile = self._getDefaultMetaData()
        return rndrjob.RndrJob(mdfile, frange, renderer, self._factories)

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
        return os.path.join(cr_utils.getAssetsPath(), 'default.yml')

    def _writeDefaultAssets(self, job):
        defaultscene = os.path.join(cr_utils.getAssetsPath(), 'default_scene.rib')
        job.copyAssetToDirectory(defaultscene)
        defaultcam = os.path.join(cr_utils.getAssetsPath(), 'default_camera.rib')
        job.copyAssetToDirectory(defaultcam)
        defaultlighting = os.path.join(cr_utils.getAssetsPath(), 'default_lighting.rib')
        job.copyAssetToDirectory(defaultlighting)
        defaultshader = os.path.join(cr_utils.getAssetsPath(), 'matte.sl')
        job.copyAssetToDirectory(defaultshader)
        ao = os.path.join(cr_utils.getAssetsPath(), 'occlusionlight.sl')
        job.copyAssetToDirectory(ao)
        colorbleeding = os.path.join(cr_utils.getAssetsPath(), 'colorbleedinglight.sl')
        job.copyAssetToDirectory(colorbleeding)

    def _copyJobMetaDataToPath(self, job, outpath):
        shutil.copy2(job.getMetaData().filename, outpath)
