import datetime, os, logging, shutil, imghdr

import chronorender.metadata as md
import rndr_doc as rd
import ribgenerator as ribgen
import ri_stream as ri
from chronorender.finder import FinderFactory, AssetNotFoundException

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
        self._outputpath    = os.path.abspath(os.path.split(infile)[0])
        self._outputdirs    = { 'output': 'OUTPUT', 
                                'shader': 'SHADERS', 
                                'script': 'SCRIPTS', 
                                'archive': 'ARCHIVES', 
                                'log':  'LOG',
                                'texture' : 'TEXTURES'
                                }
        self._relative       = False

        self._logfilename   = os.path.join(os.path.join(self._outputpath, 'LOG'), 'log_' + str(self._timecreated) + '.log')
        self._logger        = None

        self._renderer      = None

    def setOutputPath(self, path):
        self._outputpath = path

    def getSpecificOutputPath(self, typename=""):
        if typename == "":
            return self._outputpath
        else: 
            return os.path.join(self._outputpath, self._outputdirs[typename])

    def createOutDirs(self):
        log_msg = ""
        if not os.path.exists(self._outputpath): 
            os.makedirs(self._outputpath)
            # log_msg = 'created dir: ' + path + '\n'
            # self._writeToLog(log_msg)

        dirs = []
        for key, val in self._outputdirs.iteritems():
            dirs.append(os.path.join(self._outputpath,val))
        for di in dirs:
            if not os.path.exists(di):
                log_msg += di + '\n'
                os.makedirs(di)
                # log_msg = 'created dir: ' + di + '\n'
                # self._writeToLog(log_msg)

    def run(self):
        self.createOutDirs()
        # self._openLogFile()
        prevdir = os.getcwd()
        os.chdir(self._outputpath)
        self._rndrdoc.resolveAssets(self._createAssetFinder())
        self._rndrdoc.outdir = self._outputdirs['output'] if self._relative \
                else self.getSpecificOutputPath('output')
        self._outputpath
        self._startRenderer()
        for i in range(self._frames[0], self._frames[1]+1):
            name = self._rndrdoc.getOutputFilePath(i)
            # self._writeToLog('starting render ' + name + ' at: ' + str(datetime.datetime.now()))
            self._rndrdoc.render(self._renderer, i)
            # self._writeToLog('finished render ' + name + ' at: ' + str(datetime.datetime.now()))
        # self._closeLogFile()
        os.chdir(prevdir)

    def makeAssetsRelative(self):
        self.updateAssets()
        # currassets = self._getCurrentAssets()
        # for asset in self._rndrdoc.assetpaths:
            # if asset not in currassets:
                # self._copyAssetToDirectory(asset)

    def updateAssets(self):
        prevdir = os.getcwd()
        os.chdir(self._outputpath)
        paths = self._rndrdoc.resolveAssets(self._createAssetFinder())
        currassets = self._getCurrentAssets()
        for path in paths:
            if path not in currassets:
                self._copyAssetToDirectory(path)
        os.chdir(prevdir)

    def _copyAssetToDirectory(self, asset):
        filename, ext = os.path.splitext(asset)
        try:
            if ext == ".sl":
                shutil.copy2(asset, self.getSpecificOutputPath('shader'))
            elif ext == ".py":
                shutil.copy2(asset, self.getSpecificOutputPath('script'))
            elif ext == ".rib":
                shutil.copy2(asset, self.getSpecificOutputPath('archive'))
            elif imghdr.what(asset) != none:
                shutil.copy2(asset, self.getSpecificOutputPath('texture'))
        except:
            pass

    def _getCurrentAssets(self):
        out = []
        out.extend(self._dirWalkToList(self.getSpecificOutputPath('shader')))
        out.extend(self._dirWalkToList(self.getSpecificOutputPath('script')))
        out.extend(self._dirWalkToList(self.getSpecificOutputPath('archive')))
        out.extend(self._dirWalkToList(self.getSpecificOutputPath('texture')))
        return out

    def _dirWalkToList(self, path):
        out = []
        for root, dirs, files in os.walk(path):
            out.extend([os.path.join(root,f) for f in files])
        return out

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

    def _createAssetFinder(self):
        if self._relative:
            return FinderFactory.build(self._rndrdoc.getSearchPaths(), os.path.split(self._metadata.filename)[0])
        return FinderFactory.build(self._rndrdoc.getSearchPaths())

    def _startRenderer(self, outstream=''):
        # self._writeToLog('starting renderer')
        self._renderer = ri.RiStream(outstream)

