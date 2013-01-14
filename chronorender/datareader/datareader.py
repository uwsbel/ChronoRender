from cr_object import Object

class DataReader(Object):
    @staticmethod
    def getTypeName():
        return "datareader"

    def __init__(self):
        return

def build(**kwargs):
    return DataReader(**kwargs)
