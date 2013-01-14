# from chronorender.cr_object import Renderable

from geometry import Geometry

class Sphere(Geometry):
    @staticmethod
    def getTypeName():
        return "sphere"

    def __str__(self):
        return 'sphere'

def build(**kwargs):
    return Sphere(**kwargs)
