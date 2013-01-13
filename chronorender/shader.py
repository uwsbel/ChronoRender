from cr_object import Object

class ShaderException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Shader(Object):

    def __init__(self, *args, **kwargs):
        super(Shader,self).__init__(*args, **kwargs)

        self.shdrparams = {}

    def _initMembersDict(self):
        self._members['type']   = [str, 'Surface']
        self._members['name']   = [str, 'plastic']

    def getTypeName(self):
        return 'shader'
