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

    def writeJobToDisk(self, job, dest):
        outpath = os.path.join(dest, "RENDERMAN")
        job.setOutputPath(outpath)
        job.createOutDirs()
        self._writeDefaultAssets()
        self._copyJobMetaDataToPath(job, outpath)

    def createJob(self, mdfile=None):
        if not mdfile:
            mdfile = self._getDefaultMetaData()
        return rndrjob.RndrJob(mdfile, self._factories)

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

    def _writeDefaultAssets(self):
        defaultscene = os.path.join(cr_utils.getAssetsPath(), 'default_scene.rib')
        job.copyAssetToDirectory(defaultscene)
        defaultcam = os.path.join(cr_utils.getAssetsPath(), 'default_camera.rib')
        job.copyAssetToDirectory(defaultcam)
        defaultlighting = os.path.join(cr_utils.getAssetsPath(), 'default_lighting.rib')
        job.copyAssetToDirectory(defaultlighting)

    def _copyJobMetaDataToPath(self, job, oupath):
        shutil.copy2(job.getMetaData().filename, outpath)
