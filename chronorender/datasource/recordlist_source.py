
import datasource_node as dsn

class RecordListSourceNode(dsn.DataSourceNode):
    """Source node that feeds records (dictionary objects) from a list (or any other iterable)
    object."""

    node_info = {
        "label" : "Record List Source",
        "description" : "Provide list of dict objects as data source.",
        "protected": True,
        "attributes" : [
            {
                 "name": "a_list",
                 "description": "List of records represented as dictionaries."
            },
            {
                 "name": "fields",
                 "description": "Fields in the list."
            }
        ]
    }

    def __init__(self, a_list=None, fields=None, **kwargs):
        super(RecordListSourceNode, self).__init__(datasrc=None, **kwargs)
        if a_list:
            self.list = a_list
        else:
            self.list = []
        self.fields = fields

    @property
    def output_fields(self):
        if not self.fields:
            raise ValueError("Fields are not initialized")
        return self.fields

    @property
    def rows(self):
        return []

    @property
    def records(self):
        return self.list

    def initialize(self):
        return

    def finalize(self):
        return

    def run(self):
        for record in self.list:
            self.put_record(record)
