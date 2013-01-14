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

    def findAll(self, name):
        return self._mdreader.findAll(name)
