from cr_object import Object

class DataParser(Object):
    @staticmethod
    def getTypeName():
        return "dataparser"

    def __init__(self):
        return

def build(**kwargs):
    return DataParser(**kwargs)
