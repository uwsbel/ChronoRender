from geometry import Geometry

class Cube(Geometry):
    @staticmethod
    def getTypeName():
        return "cube"

    def __str__(self):
        return 'cube'

def build():
    return Cube()
