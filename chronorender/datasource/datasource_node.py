import data.nodes.base

class DataSourceNode(data.nodes.base.SourceNode):

    node_info = {
        "label" : "Null Data Source",
        "description" : "base class",
        "protected": False,
        "attributes" : [
            {
                 "name": "fields",
                 "description": "Fields in the list."
            }
        ]
    }

    def __init__(self, datasrc, *args, **kwargs):
        super(data.nodes.base.SourceNode, self).__init__()
        
        self._datasrc = datasrc
        self._fields = None
        self._args = args
        self._kwargs = kwargs

    @property
    def output_fields(self):
        return self._datasrc.fields

    def __set_fields(self, fields):
        self._fields = fields
        if self._datasrc:
            self._datasrc.fields = fields

    def __get_fields(self):
        return self._fields

    @property
    def rows(self):
        return self._datasrc.rows()

    @property
    def records(self):
        return self._datasrc.records()

    fields = property(__get_fields, __set_fields)

    def initialize(self):
        self._datasrc.initialize()

    def add_output(self, pipe):
        if pipe not in self.outputs:
            self.outputs.append(pipe)
        else:
            raise Exception("Output %s already connected" % pipe)

    def run(self):
        for row in self._datasrc.records():
            self.put_record(row)

    def finalize(self):
        self._datasrc.finalize()
