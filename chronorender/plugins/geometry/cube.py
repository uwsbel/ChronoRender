from geometry import Geometry

class Cube(Geometry):
    @staticmethod
    def getTypeName():
        return "cube"

    def render(self, ri, *args, **kwargs):
        ri.RiSphere(1,-1,1,360)

def build(**kwargs):
    return Cube(**kwargs)
