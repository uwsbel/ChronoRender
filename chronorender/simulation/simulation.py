from cr_object import Scriptable

class Simulation(Scriptable):
    @staticmethod
    def getTypeName():
        return "simulation"

    def __init__(self):
        return

def build(**kwargs):
    return Simulation(**kwargs)
