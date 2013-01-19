import datetime, os, logging

import chronorender.metadata as md
import rndr_doc as rd
import ribgenerator as ribgen
import ri_stream as ri

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
        self._ribgen        = ribgen.RIBGenerator(factories, self._metadata)
        self._timecreated   = datetime.datetime.now()
        self._frames        = self._rndrdoc.getFrameRange()
        self._outputpath    = self._rndrdoc.getOutputFileDir()
        self._outputdirs    = ['OUTPUT', 'SHADERS', 'SCRIPTS', 'ASSETS', 'LOG']

        self._logfilename   = os.path.join(os.path.join(self._outputpath, 'LOG'), 'log_' + str(self._timecreated) + '.log')
        self._logger        = None

        self._renderer      = None

    def run(self):
        self._createOutDirs()
        self._openLogFile()
        self._startRenderer()
        for i in range(self._frames[0], self._frames[1]+1):
            name = self._rndrdoc.getOutputDataFilePath(i)
            self._writeToLog('starting render ' + name + ' at: ' + str(datetime.datetime.now()))
            self._rndrdoc.render(self._renderer, framenumber=i)
            self._writeToLog('finished render ' + name + ' at: ' + str(datetime.datetime.now()))
        self._closeLogFile()

    def _writeToLog(self, content):
        # self._logger.info('starting render ' + name + ' at: ' + str(datetime.datetime.now()))
        self._logger.write(content+'\n')   

    def _openLogFile(self):
        self._logger= open(self._logfilename, 'a')

        # self._logger = logging.getLogger('')
        # hdlr = logging.FileHandler(self._logfilename)
        # formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        # hdlr.setFormatter(formatter)
        # self._logger.addHandler(hdlr)
        # self._logger.setLevel(logging.INFO)

    def _closeLogFile(self):
        self._logger.close()

    def _startRenderer(self, outstream=''):
        self._writeToLog('starting renderer')
        self._renderer = ri.RiStream(outstream)

    def _createOutDirs(self):
        log_msg = ""
        if not os.path.exists(self._outputpath): 
            os.makedirs(self._outputpath)
            log_msg = 'created dir: ' + self._outputpath + '\n'
            self._writeToLog(log_msg)

        dirs = [os.path.join(self._outputpath, d) for d in self._outputdirs]
        for di in dirs:
            if not os.path.exists(di):
                log_msg += di + '\n'
                os.makedirs(di)
                log_msg = 'created dir: ' + di + '\n'
                self._writeToLog(log_msg)
