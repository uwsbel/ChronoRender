from cr_object import Object

class RndrPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrPass(Object):

    def __init__(self, *args, **kwargs):
        super(RndrPass,self).__init__(*args, **kwargs)

        self.rndrobjects = []

    def _initMembersDict(self):
        self._members['name']           = [str, 'nothing']
        self._members['scene']          = [str, 'nothing']
        self._members['lighting']       = [str, 'nothing']
        self._members['resolution']     = ['spalist', [-1,-1]]
        self._members['renderobjs']     = ['spalist', ['default']]

    def getTypeName(self):
        return 'renderpass'

    def render(self, data):
        return str(data)
