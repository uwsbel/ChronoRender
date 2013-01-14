from cr_object import Object

class _MDReader(Object):
    @staticmethod
    def getTypeName():
        return "mdreader"

    @staticmethod
    def _convertElemToDict(node):
        return

    @staticmethod
    def _convertDictToElem(node):
        return

    @staticmethod
    def _convertDictToKwargs(args):
        return

    def findAll(self, name):
        return []

    def _parseString(self, instring):
        return

    def _parseFile(self, infile):
        return
