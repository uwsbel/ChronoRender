from cr_object import Object

class DataProcessor(Object):
    @staticmethod
    def getTypeName():
        return "dataprocessor"

    def __init__(self):
        return

def build(**kwargs):
    return DataSource(**kwargs)
