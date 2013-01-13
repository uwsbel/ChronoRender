from chronorender.cr_object import Renderable

class Sphere(Renderable):
    @staticmethod
    def getTypeName():
        return "sphere"

    def __str__(self):
        return 'sphere'

def build():
    return Sphere()
