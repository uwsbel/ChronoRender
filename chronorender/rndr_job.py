import datetime, os, logging, glob, __main__

import chronorender.cr_object as cr_object
import chronorender.cr_utils as cr_utils
import chronorender.metadata as md
import chronorender.rndr_doc as rd
import chronorender.renderer as cr
import chronorender.ri as ri
import chronorender.distributed as cd
from chronorender.rndr_job_assetmanager import RndrJobAssetManager

class RndrJobException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrJob():
    _RendererFactory = cr.RendererFactory()
    _DistributedFactory = cd.DistributedFactory()

    def __init__(self, infile, stream, factories):
        self.stream         = stream
        self.typefilter     = []
        self.frames         = None
        self.bOptions       = True
        self._factories     = factories
        self._metadata      = md.MetaData(infile)
        self._rndrdoc       = rd.RndrDoc(self._factories, self._metadata)
        self._rootdir       = os.path.abspath(os.path.split(self._metadata.filename)[0])
        self._timecreated   = datetime.datetime.utcnow()
        self._renderer      = None
        self._assetman      = RndrJobAssetManager(self._rootdir, self._rndrdoc)
        # print "self.stream = " + self.stream

    def run(self):
        # print "run self.stream = " + self.stream
        self._assetman.createOutDirs()
        prevdir = os.getcwd()
        try:
            os.chdir(self._rootdir)
            self._resolveAssets()
            self._render()
        except Exception as err:
            print err
            raise err
        finally:
            os.chdir(prevdir)

    def _resolveAssets(self):
        self._assetman.updateAssets()
        self._assetman.compileShaders(self.stream)
        self._assetman.convertTextures(self.stream)
        self._verifyFrameRange()

    def _render(self):
        print "_render " + self.stream
        self._renderer = RndrJob._RendererFactory.build(self.stream)
        self._startRenderer()
        if self.bOptions:
            self._renderOptions()
        self._renderFrames()
        self._stopRenderer()

    def _renderOptions(self):
        cr_paths = cr_utils.getCRAssetPaths()
        cr_pathsstr = reduce(lambda x, y: str(x) + ":" + str(y), cr_paths)
        cr_pathsstr += ":"
        self._renderer.Option("searchpath", {"shader":
                cr_pathsstr + self._assetman.getOutPathFor("shader") + ":@"})
        self._renderer.Option("searchpath", {"procedural" :
                cr_pathsstr + self._assetman.getOutPathFor("script") + ":@"})
        self._renderer.Option("searchpath", {"texture":
                cr_pathsstr + self._assetman.getOutPathFor("texture") + ":@"})
        self._renderer.Option("searchpath", {"archive":
                cr_pathsstr + self._assetman.getOutPathFor("archive") + ":@"})

    def _renderFrames(self):
        for framenum in range(self.frames[0], self.frames[1]+1):
            self._rndrdoc.render(self._renderer, framenum, self.typefilter)

    def _verifyFrameRange(self):
        if self.frames:
            if len(self.frames) != 2:
                raise RndrJobException("invalid frames: " + str(self.frames))

            if self.frames[0] < 0 or self.frames[1] < 0:
                raise RndrJobException("invalid frames: " + str(self.frames))

            if self.frames[1] > self.frames[1]:
                self.frames[1] = self.frames[1]
            self.frames = self.frames
        else:
            self.frames = self._assetman.getFrameRange()

    def setOutputPath(self, path):
        self._assetman.setOutPath(path)

    def createOutDirs(self):
        self._assetman.createOutDirs()

    def makeAssetsRelative(self):
        self.updateAssets()

    def updateAssets(self):
        self._assetman.updateAssets()

    def copyAssetToDirectory(self, asset):
        self._assetman.copyAssetToDirectory(asset)

    def submit(self, prog):
        prevdir = os.getcwd()
        try:
            os.chdir(self._rootdir)
            dist = self._getDistributedInterface()
            job = self._getConfiguredDistJob(dist, prog)
            dist.initialize()
            dist.submit(job)
            dist.wait(job)
            dist.end()
        except Exception as err:
            raise err
        finally:
            os.chdir(prevdir)

    def _getDistributedInterface(self):
        distinfo = self._metadata.singleFromType(cd.Distributed, bRequired=False)
        dist = None
        if distinfo:
            dist = cr_object.Object(basename=cd.Distributed.getTypeName(), 
                    factories=self._factories, **distinfo)
        else:
            dist = cr_object.Object(basename=cd.Distributed.getTypeName(), 
                    factories=self._factories)
        return dist

    def _getConfiguredDistJob(self, dist, prog):
        job = dist.createJobTemplate()
        job.name = "render_" + self._timecreated.strftime("%y_%m_%d_%s")
        job.queue = "prman"
        job.prog = self._configureProgForJob(prog)
        job.wd = self._rootdir
        out = dist.finalizeJob(job, self._assetman)
        return job

    def _configureProgForJob(self, prog):
        print "_configureProgForJob self.stream1 = " + self.stream
        prog.args['metadata'] = self._metadata.filename
        prog.args['framerange'] = str(self.frames[0]) + " " + str(self.frames[1])
        prog.args['renderer'] = self.stream
        print "_configureProgForJob self.stream2 = " + self.stream
        return prog

    def _startRenderer(self):
        self._renderer.init()
        self._renderer.startRenderContext()

    def _stopRenderer(self):
        self._renderer.stopRenderContext()
        self._renderer.cleanup()

    def getMetaData(self):
        return self._metadata
