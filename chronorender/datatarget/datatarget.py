# import data.ds.base
from chronorender.data.nodes.base import TargetNode
# Should implement:
# * fields
# * prepare()
# * rows() - returns iterable with value tuples
# * records() - returns iterable with dictionaries of key-value pairs

class DataTargetException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class DataTarget(TargetNode):
    node_info = {
        "label" : "blah",
        "description" : "gorb",
        "attributes" : [ ]
    }

    @staticmethod
    def getInstanceQualifier():
        return "type"

    @staticmethod
    def getTypeName():
        return "datatarget"

    def getBaseName(self):
        return TargetNode.getTypeName()

    @property
    def data(self):
        return self._data

    def __init__(self,  *args, **kwargs):
        super(DataTarget,self).__init__(*args, **kwargs)

        self._data = []

    def _initMembersDict(self):
        super(DataTarget, self)._initMembersDict()

    def append(self, obj):
        self._data.append(obj)

    def initialize(self):
        return

    def run(self):
        for row in self.input.records():
            self.append(row)

    def finalize(self):
        return

def build(**kwargs):
    return DataTarget(**kwargs)
