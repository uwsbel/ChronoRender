from geometry import Geometry

class Cube(Geometry):
    @staticmethod
    def getTypeName():
        return "cube"

    def __str__(self):
        return 'cube'

    def _initMembersDict(self):
        super(Cube, self)._initMembersDict()

    def render(self, rib, *args, **kwargs):
        rib.Sphere(1,-1,1,360)

def build(**kwargs):
    return Cube(**kwargs)
