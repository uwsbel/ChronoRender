from cr_object import Object
import glob
import os
import re

class RndrSettingsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrSettings(Object):

    @staticmethod
    def getTypeName():
        return "settings"

    def __init__(self, *args, **kwargs):
        super(RndrSettings,self).__init__(*args, **kwargs)

        self._resolveIOPath('in')
        self._resolveIOPath('out')
        self._resovleSearchPathsToAbsolute()
        self._resolveOutputFormat()
        self._resolvePadding()

    def _initMembersDict(self):
        self._members['padding']    = [int, 1]
        self._members['delim']      = [str, ',']
        self._members['out']        = [str, './out_####.tif']
        self._members['fileformat'] = [str, 'tif']
        self._members['in']         = [str, './*.dat']
        self._members['scaling']    = [float, 1.0]
        self._members['radians']    = [bool, False]
        self._members['searchpaths'] = ['collist', ['./']]
        self._members['framerange'] = ['spalist', [0, 0]]
        self._members['dataformat'] = ['comlist', ['ID', 'POS_X', 'POS_Y', 'POS_Z']]

    def getInputDataFiles(self):
        return glob.glob(self.getMember('in'))

    def getOutputDataFilePath(self, framenumber):
        padd = self.getMember('padding')

        frame = str(framenumber)
        while len(frame) < padd:
            frame += '0'
        outfile = self.getMember('out')
        return re.sub('#+', frame, outfile)
    
    def getSearchPaths(self):
        return self.getMember('searchpaths')

    def _resolveIOPath(self, membername):
        data_re = self.getMember(membername)
        dpath, dre = os.path.split(data_re)
        abspath = os.path.abspath(dpath)
        if os.path.exists(abspath) != True:
            raise RndrSettingsException('path DNE for ' + membername + ': ' + abspath)
        self.setMember(membername, os.path.join(abspath,dre))

    def _resovleSearchPathsToAbsolute(self):
        resolved_paths = []
        paths = self.getMember('searchpaths')
        for i in range(0,len(paths)):
            if os.path.exists(paths[i]):
                resolved_paths.append(os.path.abspath(paths[i]) + os.sep)
        self.setMember('searchpaths', resolved_paths)

    def _resolveOutputFormat(self):
        self.setMember('fileformat', os.path.splitext(self.getMember('out'))[1])

    def _resolvePadding(self):
        filename = os.path.split(self.getMember('out'))[1]
        self.setMember('padding', len(re.findall('#+', filename)[-1]))
