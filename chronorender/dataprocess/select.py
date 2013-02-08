import dataprocess as dp

class SelectNode(dp.DataProcess):
    node_info = {
        "label" : "Select",
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
        return "select"

    def __init__(self, condition = None, discard = False, **kwargs):
        """Creates and initializes selection node
        """
        super(SelectNode, self).__init__(**kwargs)
        # self.condition = condition
        self.condition = condition
        self.discard = discard

    def _initMembersDict(self):
        super(SelectNode, self)._initMembersDict()

        self._members['condition'] = [str,'']

    def updateMembers(self):
        super(SelectNode, self).updateMembers()
        self.setMember('condition', self.condition)


    def initialize(self):
        if isinstance(self.condition, basestring):
            self._expression = compile(self.condition, "SelectNode condition", "eval")
            self._condition_callable = self._eval_expression
        else:
            self._condition_callable = self.condition

    def _eval_expression(self, **record):
        return eval(self._expression, None, record)

    def run(self):
        for record in self.input.records():
            if self._condition_callable(**record):
                self.put_record(record)

def build(**kwargs):
    return SelectNode(**kwargs)
