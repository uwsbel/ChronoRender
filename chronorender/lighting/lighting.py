from cr_object import Scriptable

class Lighting(Scriptable):
    @staticmethod
    def getTypeName():
        return "lighting"

    def __init__(self):
        return

def build(**kwargs):
    return Lighting(**kwargs)
