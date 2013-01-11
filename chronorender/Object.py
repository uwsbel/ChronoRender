

class ObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Object(object):

    def __init__(self, *args, **kwargs):
        self._params = {}

    def __str__(self):
        return str(self._params)
