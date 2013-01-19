from cr_object import Scriptable

class RenderPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RenderPass(Scriptable):

    @staticmethod
    def getTypeName():
        return "renderpass"

    def __init__(self, *args, **kwargs):
        super(RenderPass,self).__init__(*args, **kwargs)

        self.rndrobjects = []

    def _initMembersDict(self):
        self._members['name']           = [str, 'nothing']
        self._members['scene']          = [str, 'nothing']
        self._members['lighting']       = [str, 'nothing']
        self._members['resolution']     = ['spalist', [-1,-1]]
        self._members['renderobjs']     = ['spalist', ['default']]

    def render(self, rib, **kwargs):
        return str(data)

    def getOutput(self):
        return "out"

def build(**kwargs):
    return RenderPass(**kwargs)
