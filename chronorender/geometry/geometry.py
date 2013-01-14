from cr_object import Scriptable

class GeometryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Geometry(Scriptable):

    @staticmethod
    def getTypeName():
        return "geometry"

    def __init__(self, *args, **kwargs):
        super(Geometry,self).__init__(*args, **kwargs)

    def _initMembersDict(self):
        return

def build(**kwargs):
    return Geometry(**kwargs)
