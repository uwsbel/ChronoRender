from cr_object import Object

class GeometryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Geometry(Object):

    def __init__(self, *args, **kwargs):
        super(Geometry,self).__init__(*args, **kwargs)

        self.geoparams = {}

    def _initMembersDict(self):
        self._members['type']   = [str, 'Surface']

    def getTypeName(self):
        return 'geometry'
