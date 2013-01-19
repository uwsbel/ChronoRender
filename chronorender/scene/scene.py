from cr_object import Scriptable

class Scene(Scriptable):
    @staticmethod
    def getTypeName():
        return "scene"

    def __init__(self, *args, **kwargs):
        super(Scene,self).__init__(*args, **kwargs)

def build(**kwargs):
    return Scene(**kwargs)
