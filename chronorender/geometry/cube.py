from chronorender.cr_object import Renderable

class Cube(Renderable):
    @staticmethod
    def getTypeName():
        return "cube"

    def __str__(self):
        return 'cube'

def build():
    return Cube()
