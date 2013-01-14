from _mdreader import _MDReader
import yaml
import copy

class _MDYAML(_MDReader):
    @staticmethod
    def getTypeName():
        return "mdreaderyaml"

    @staticmethod
    def _convertElemToDict(node):
        return copy.deepcopy(node)

    @staticmethod
    def _convertDictToElem(node):
        return node

    @staticmethod
    def _convertDictToKwargs(args):
        out = {}
        return out

    def __init__(self, inxmlfile):
        self._filename = inxmlfile
        self._root = []

        self._parseFile(inxmlfile)

    def _parseString(self, instring):
        gen = yaml.load_all(instring)
        for data in gen:
            self._root = copy.deepcopy(data)

    def _parseFile(self, infile):
        stream = open(infile, 'r')
        gen = yaml.load_all(stream)
        for data in gen:
            self._root.append(copy.deepcopy(data))

    def findAll(self, name):
        out = []

        for elem in self._root:
            for key, val in elem.iteritems():
                if key == name:
                    out.append(val)
        return out
