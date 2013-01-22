import os, re

from cr_object import Object
from cr_types import intlist, strlist

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

        self.padding       = self.getMember('padding')
        self.out           = self.getMember('out')
        self.fileformat    = self.getMember('fileformat')
        self.searchpaths   = self.getMember('searchpaths')
        self.framerange    = self.getMember('framerange')


        self._resolveOutputFormat()
        self._resolvePadding()

    def _initMembersDict(self):
        super(RenderSettings, self)._initMembersDict()
        self._members['padding']        = [int, 1]
        self._members['out']            = [str, './']
        self._members['fileformat']     = [str, 'tif']
        self._members['searchpaths']    = [strlist, ['./']]
        self._members['framerange']     = [intlist, [0, 0]]

    # def _resolveOutputPath():
        # dpath, dre = os.path.split(self._out)
        # abspath = os.path.abspath(dpath)
        # outpath = os.path.join(abspath, dre)
        # self._out = outpath

    def _resolveOutputFormat(self):
        self._fileformat =  os.path.splitext(self.getMember('out'))[1]

    def _resolvePadding(self):
        if self.padding < len(str(self.framerange[1])):
            self.padding = len(str(self.framerange[1]))
        # filename = os.path.split(self._out)[1]
        # self._padding = len(re.findall('#+', filename)[-1])

def build(**kwargs):
    return RenderSettings(**kwargs)
