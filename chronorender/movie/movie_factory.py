from prman import PRMan
from aqsis import Aqsis
from stdout import Stdout

class MovieFactoryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MovieFactory():
    @staticmethod
    def build(renderername):
        if renderername == PRMan.getName():
            return PRMan()
        elif renderername == Aqsis.getName():
            return Aqsis()
        elif renderername == Stdout.getName():
            return Stdout()
        else:
            raise MovieFactoryException('renderer: \"' + renderername + '\" is not supported')
