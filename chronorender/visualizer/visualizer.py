from cr_object import Scriptable

class Visualizer(Scriptable):
    @staticmethod
    def getTypeName():
        return "visualizer"

    def __init__(self):
        return

def build(**kwargs):
    return Visualizer(**kwargs)
