import chronorender.dataprocess as dp

from chronorender.data.metadata import FieldMap, FieldList, Field
from chronorender.data.common import FieldError

class DeriveNode(dp.DataProcess):
    node_info = {
        "label" : "Derive",
        "description" : "Select or discard records from the stream according to a predicate.",
        "output" : "same fields as input",
        "attributes" : [
            {
                 "name": "condition",
                 "description": "Callable or a string with python expression that will evaluate to "
                                "a boolean value"
            },
            {
                "name": "discard",
                 "description": "flag whether the records matching condition are discarded or included",
                 "default": "False"
            }
        ]
    }

    @staticmethod
    def getTypeName():
        return "derive"

    node_info = {
        "label" : "Derive Node",
        "description" : "Derive a new field using an expression.",
        "attributes" : [
            {
                 "name": "field_name",
                 "description": "Derived field name",
                 "default": "new_field"
            },
            {
                 "name": "formula",
                 "description": "Callable or a string with python expression that will evaluate to "
                                "new field value"
            },
            {
                "name": "analytical_type",
                 "description": "Analytical type of the new field",
                 "default": "unknown"
            },
            {
                "name": "storage_type",
                 "description": "Storage type of the new field",
                 "default": "unknown"
            }
        ]
    }


    def __init__(self, formula = None, field_name = "new_field", analytical_type = "unknown",
                        storage_type = "unknown", **kwargs):
        """Creates and initializes selection node
        """
        super(DeriveNode, self).__init__(**kwargs)
        self.formula = formula
        self.field_name = field_name
        self.analytical_type = analytical_type
        self.storage_type = storage_type
        self._output_fields = None

    @property
    def output_fields(self):
        return self._output_fields

    def initialize(self):
        if isinstance(self.formula, basestring):
            self._expression = compile(self.formula, "DeriveNode expression", "eval")
            self._formula_callable = self._eval_expression
        else:
            self._formula_callable = self.formula

        self._output_fields = FieldList()

        for field in self.input.fields:
            self._output_fields.append(field)

        new_field = Field(self.field_name, analytical_type = self.analytical_type,
                                  storage_type = self.storage_type)
        self._output_fields.append(new_field)

    def _eval_expression(self, **record):
        return eval(self._expression, None, record)

    def run(self):
        for record in self.input.records():
            if self._formula_callable:
                record[self.field_name] = self._formula_callable(**record)
            else:
                record[self.field_name] = None

            self.put_record(record)

def build(**kwargs):
    return DeriveNode(**kwargs)
