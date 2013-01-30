import os.path as path

from cr_renderable import Renderable

class DisplayException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Display(Renderable):

    @staticmethod
    def getTypeName():
        return "display"

    def __init__(self, *args, **kwargs):
        super(Display,self).__init__(*args, **kwargs)

        self.output     = self.getMember('output')
        self.outtype    = self.getMember('outtype')
        self.mode       = self.getMember('mode')
        self._fileout   = self.output

    def _initMembersDict(self):
        super(Display, self)._initMembersDict()
        self._members['output']     = [str, 'default']
        self._members['outtype']    = [str, 'file']
        self._members['mode']       = [str, 'rgba']

    def getOutputs(self):
        return [self._fileout]

    def render(self, rib, outpath='', postfix='', **kwargs):
        self._fileout = self._evalOutName(outpath, postfix)
        rib.Display(self._fileout, self.outtype, self.mode)

    def _evalOutName(self, outpath, postfix):
        vals = self.output.split('.')
        out = vals[0] + "." + postfix
        if len(vals) > 1:
            for i in range(1,len(vals)):
                out += "." + vals[i]
        return path.join(outpath, out)


def build(**kwargs):
    return Display(**kwargs)
