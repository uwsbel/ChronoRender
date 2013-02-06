from chronorender.data.nodes.base import Node
from chronorender.cr_object import Object

class DataProcess(Node, Object):
    node_info = {
        "label" : "PassThrough (default)",
        "description" : "does nothing",
        "output" : "same fields as input",
        "attributes" : []
    }

    @staticmethod
    def getTypeName():
        return "dataprocess"

    def __init__(self, name="default", *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        super(Object, self).__init__(*args, **kwargs)
        self.name = name

    def initialize(self):
        return

    # pass through
    def run(self):
        for record in self.input.records():
            self.put_record(record)

def build(**kwargs):
    return DataProcess(**kwargs)
