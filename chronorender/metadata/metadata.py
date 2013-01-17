import pprint

from itertools import groupby
from mdreader_factory import MDReaderFactory

class MetaDataException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MetaData():
    def __init__(self, infile=''):
        self._filename = infile
        self._mdreader = MDReaderFactory.build(infile)

    def __str__(self):
        return str(self._mdreader)

    def findAll(self, name):
        return self._mdreader.findAll(name)

    def singleFromClassType(self, elemtype, bRequired=True):
        elems = self.findAll(elemtype.getTypeName())
        if len(elems) != 1 and bRequired:
            raise MetaDataException('not only ONE ' + elemtype.getTypeName() + ' in metadata')
        return elems[0]
        # return self._constructObject(elems[0], elemtype)

    def listFromClassType(self, elemtype, bRequired=True):
        elems = self.findAll(elemtype.getTypeName())
        if len(elems) <= 0 and bRequired:
            raise MetaDataException('no ' + elemtype.getTypeName() + ' in metadata')

        return elems
        # out = []
        # for inst in elems:
            # out.append(self._constructObject(inst, elemtype))
        # return out
