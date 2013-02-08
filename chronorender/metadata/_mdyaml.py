from _mdreader import _MDReader

import chronorender.thirdparty.yaml as tyaml
import pprint, copy, itertools, os.path

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
        self._root = {}

        if os.path.exists(inxmlfile):
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

        if _MDReader._root_name not in self._root:
            raise Exception
        self._root = self._root[_MDReader._root_name]

        # gen = yaml.load(stream)
        # for data in gen:
            # self._root.append(copy.deepcopy(data))

    def findAll(self, name):
        out = []
        for key, val in self._root.iteritems():
            if key == name:
                out = _MDYAML._convertElemToDict(val)
        return out

    def getElementsDict(self):
        out = {}
        for key, val in self._root.iteritems():
            elem = _MDYAML._convertElemToDict(val)
            if key in out:
                for e in elem:
                    out[key].append(e)
            else:
                out[key] = elem
        return out

    def addElement(self, name, elemdict):
        if name in self._root:
            self._root[name].append(elemdict)
            return
        self._root[name] = [elemdict]

    def writeToDisk(self, path=None):
        if not path:
            path = self._filename
        stream = file(path, 'w')
        out_root = {_MDReader._root_name : self._root}
        tyaml.dump(out_root, stream)
