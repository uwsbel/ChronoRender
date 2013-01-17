from _mdreader import _MDReader

import thirdparty.yaml as tyaml
import pprint, copy, itertools

class _MDYAML(_MDReader):
    @staticmethod
    def getTypeName():
        return "mdreaderyaml"

    @staticmethod
    def _flatten(darray):
        merge = list(itertools.chain(darray))
        # for i in range(0,len(merge)):
            # if isinstance(merge[i], list):
                # merge[i] = _MDYAML._flatten(*merge[i])
        # merge = list(itertools.chain(*merge))
        return merge

    @staticmethod
    def _convertElemToDict(node):
        out = []
        if isinstance(node, list):
            out += _MDYAML._flatten(node)
        elif isinstance(node, dict):
            out.append(node)
        return out

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

    def __str__(self):
        return pprint.pformat(self._root)

    def _parseString(self, instring):
        gen = tyaml.load_all(instring)
        for data in gen:
            self._root = copy.deepcopy(data)

    def _parseFile(self, infile):
        stream = open(infile, 'r')
        self._root = tyaml.load(stream)
        # gen = yaml.load(stream)
        # for data in gen:
            # self._root.append(copy.deepcopy(data))

    def findAll(self, name):
        out = []

        if 'chronorender'not in self._root:
            raise Exception
        root = self._root['chronorender']
        for key, val in root.iteritems():
            if key == name:
                out = _MDYAML._convertElemToDict(val)
        return out
