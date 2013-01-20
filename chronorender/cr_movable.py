from cr_renderable import Renderable, RenderableException

# extended renderable, can have render scripted
class MovableException(RenderableException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Movable(Renderable):
    def __init__(self, factories=None, *args, **kwargs):
        super(Movable,self).__init__(factories=factories, *args, **kwargs)

    def __str__(self):
        return super(Movable,self).__str__()

    def getCenter(self):
        return [0.0,0.0,0.0]
