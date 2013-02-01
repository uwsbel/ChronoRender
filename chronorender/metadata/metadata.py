import pprint

import os
from mdreader_factory import MDReaderFactory

class MetaDataException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MetaData(object):
    def __init__(self, infile=''):
        self.filename = os.path.abspath(infile)
        self._mdreader = MDReaderFactory.build(infile)

    def __str__(self):
        return str(self._mdreader)

    def findAll(self, name):
        return self._mdreader.findAll(name)

    def getElementsDict(self):
        return self._mdreader.getElementsDict()

    def singleFromType(self, elemtype, bRequired=True):
        elems = self.findAll(elemtype.getTypeName())
        if len(elems) != 1:
            if bRequired:
                raise MetaDataException('not only ONE ' + elemtype.getTypeName() + ' in metadata, found: ' + str(len(elems)))
            return None
        return elems[0]
        # return self._constructObject(elems[0], elemtype)

    def listFromType(self, elemtype, bRequired=True):
        elems = self.findAll(elemtype.getTypeName())
        if len(elems) <= 0:
            if bRequired:
                raise MetaDataException('no ' + elemtype.getTypeName() + ' in metadata')
            return []
        return elems
