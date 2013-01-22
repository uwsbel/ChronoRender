import datetime, os, logging

import chronorender.metadata as md
import rndr_doc as rd
import chronorender.ri as ri
from rndr_job_assetmanager import RndrJobAssetManager

# represent a render job
class RndrJobException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrJob():
    def __init__(self, infile, factories):
        self._metadata      = md.MetaData(infile)
        self._rndrdoc       = rd.RndrDoc(factories, self._metadata)
        self._timecreated   = datetime.datetime.now()
        self._frames        = self._rndrdoc.getFrameRange()
        self._assetman      = RndrJobAssetManager(os.path.abspath(os.path.split(self._metadata.filename)[0]))

        # self._logfilename   = os.path.join(os.path.join(self._outputpath, 'LOG'), 'log_' + str(self._timecreated) + '.log')
        # self._logger        = None

        self._renderer      = None

    def run(self):
        self._assetman.createOutDirs()
        # self._openLogFile()
        prevdir = os.getcwd()
        os.chdir(self._assetman.outputpath)
        self._rndrdoc.resolveAssets(self._assetman.createAssetFinder(self._rndrdoc), 
                self._assetman.getOutPathFor('output'))
        # self._rndrdoc.outdir = self._assetman.getOutPathFor('output')

        self._startRenderer()
        self._renderOptions()
        for i in range(self._frames[0], self._frames[1]+1):
            name = self._rndrdoc.getOutputFilePath(i)
            # self._writeToLog('starting render ' + name + ' at: ' + str(datetime.datetime.now()))
            self._rndrdoc.render(self._renderer, i)
            # self._writeToLog('finished render ' + name + ' at: ' + str(datetime.datetime.now()))
        # self._closeLogFile()
        os.chdir(prevdir)

    def _renderOptions(self):
        self._renderer.RiOption("searchpath", "shader",
                self._assetman.getOutPathFor("shader"))
        self._renderer.RiOption("searchpath", "procedural",
                self._assetman.getOutPathFor("script"))
        self._renderer.RiOption("searchpath", "texture",
                self._assetman.getOutPathFor("texture"))
        self._renderer.RiOption("searchpath", "archive",
                self._assetman.getOutPathFor("archive"))

    def setOutputPath(self, path):
        self._assetman.outputpath = path

    def createOutDirs(self):
        self._assetman.createOutDirs()

    def makeAssetsRelative(self):
        self.updateAssets()

    def updateAssets(self):
        self._assetman.updateAssets(self._rndrdoc)

    def copyAssetToDirectory(self, asset):
        self._assetman._copyAssetToDirectory(asset)

    def _startRenderer(self, outstream=''):
        # self._writeToLog('starting renderer')
        self._renderer = ri.RiStream(outstream)

    # def _writeToLog(self, content):
        # self._logger.info('starting render ' + name + ' at: ' + str(datetime.datetime.now()))
        # self._logger.write(content+'\n')   

    # def _openLogFile(self):    
        # self._logger= open(self._logfilename, 'a')

        # self._logger = logging.getLogger('')
        # hdlr = logging.FileHandler(self._logfilename)
        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        # hdlr.setFormatter(formatter)
        # self._logger.addHandler(hdlr)
        # self._logger.setLevel(logging.INFO)

    # def _closeLogFile(self):
        # self._logger.close()
