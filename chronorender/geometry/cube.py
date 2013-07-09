from geometry import Geometry

class Cube(Geometry):
    @staticmethod
    def getTypeName():
        return "cube"

    def __str__(self):
        return 'cube'

    def _initMembersDict(self):
        super(Cube, self)._initMembersDict()

        self._members['side'] = [float, 1.0]

    def render(self, rib, *args, **kwargs):
        rib.Cone(1,1,360)
        # rib.Sphere(1,-1,1,360)

def build(**kwargs):
    return Cube(**kwargs)
