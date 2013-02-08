from chronorender.data.nodes.base import Node
from chronorender.cr_object import Object

class DataProcess(Object, Node):
    node_info = {
        "label" : "PassThrough (default)",
        "description" : "does nothing",
        "output" : "same fields as input",
        "attributes" : []
    }

    @staticmethod
    def getTypeName():
        return "dataprocess"

    def __init__(self, *args, **kwargs):
        super(DataProcess, self).__init__(*args, **kwargs)

        self.name = self.getMember('name')

    def _initMembersDict(self):
        super(DataProcess, self)._initMembersDict()

        self._members['name'] = [str, 'default']

    def updateMembers(self):
        super(DataProcess, self).updateMembers()

        self.setMember('name', self.name)

    def initialize(self):
        return

    # pass through
    def run(self):
        for record in self.input.records():
            self.put_record(record)

def build(**kwargs):
    return DataProcess(**kwargs)
