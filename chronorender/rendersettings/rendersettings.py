import os, re

from cr_object import Object

class RenderSettingsException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderSettings(Object):

    @staticmethod
    def getTypeName():
        return "rendersettings"

    def __init__(self, *args, **kwargs):
        super(RenderSettings,self).__init__(*args, **kwargs)

        self._padding       = 1
        self._out           = './out_####.tif'
        self._fileformat    = 'tif'
        self._searchpaths   = './'
        self._framerange    = [0, 0]

        self._setMembers()
        self._resolveIOPath('out', False)
        self._resolveOutputFormat()
        self._resolvePadding()

    def _initMembersDict(self):
        self._members['padding']        = [int, 1]
        self._members['out']            = [str, './out_####.tif']
        self._members['fileformat']     = [str, 'tif']
        self._members['searchpaths']    = ['collist', ['./']]
        self._members['framerange']     = ['spalist', [0, 0]]

    def _setMembers(self):
        self._padding       = self.getMember('padding')
        self._out           = self.getMember('out')
        self._fileformat    = self.getMember('fileformat')
        self._searchpaths   = self.getMember('searchpaths')
        self._framerange    = self.getMember('framerange')

    def _resolveIOPath(self, membername, bRequired=True):
        data_re = self.getMember(membername)
        dpath, dre = os.path.split(data_re)
        abspath = os.path.abspath(dpath)
        if not os.path.exists(abspath):
            if bRequired:
                raise RenderSettingsException('path DNE for ' + membername + ': ' + abspath)
        outpath = os.path.join(abspath, dre)
        self.setMember(membername, outpath)
        if membername == 'out':
            self._out = outpath

    def _resolveOutputFormat(self):
        self._fileformat =  os.path.splitext(self.getMember('out'))[1]
        self.setMember('fileformat', self._fileformat)

    def _resolvePadding(self):
        filename = os.path.split(self.getMember('out'))[1]
        self._padding = len(re.findall('#+', filename)[-1])
        self.setMember('padding', self._padding)

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

def build(**kwargs):
    return RenderSettings(**kwargs)
