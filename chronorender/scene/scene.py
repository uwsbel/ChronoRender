from cr_object import Scriptable

class Scene(Scriptable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self):
        return

def build(**kwargs):
    return Scene(**kwargs)
