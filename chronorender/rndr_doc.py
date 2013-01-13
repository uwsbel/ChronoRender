# contains all assests needed to start a render job

class RndrDocException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RndrDoc():
    def __init__(self):
        self.name = ''
