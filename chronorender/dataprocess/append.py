import dataprocess as dp

class AppendNode(dp.DataProcess):
    """Sequentialy append input streams. Concatenation order reflects input stream order. The
    input streams should have same set of fields."""
    node_info = {
        "label" : "Append",
        "description" : "Concatenate input streams."
    }

    @staticmethod
    def getTypeName():
        return "append"

    def __init__(self, *args, **kwargs):
        """Creates a node that concatenates records from inputs. Order of input pipes matter."""
        super(AppendNode, self).__init__(**kwargs)

    @property
    def output_fields(self):
        if not self.inputs:
            raise ValueError("Can not get list of output fields: node has no input")

        return self.inputs[0].fields

    def run(self):
        """Append data objects from inputs sequentially."""
        for pipe in self.inputs:
            for row in pipe.rows():
                self.put(row)

