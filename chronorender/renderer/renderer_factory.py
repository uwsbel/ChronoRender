
from prman import PRMan
from aqsis import Aqsis
from stdout import Stdout

class RendererFactoryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RendererFactory():
    @staticmethod
    def build(renderername):
        if renderername == PRMan.getName():
            return PRMan()
        elif renderername == Aqsis.getName():
            return Aqsis()
        elif renderername == Stdout.getName():
            return Stdout()
        else:
            raise RendererFactoryException('renderer: \"' + renderername + '\" is not supported')
