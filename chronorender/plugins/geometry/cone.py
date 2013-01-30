# from chronorender.cr_object import Renderable

from geometry import Geometry

class Cone(Geometry):
    @staticmethod
    def getTypeName():
        return "cone"

    def __init__(self, *args, **kwargs):
        super(Cone,self).__init__(*args, **kwargs)

        self.height = self.getMember('height')
        self.radius = self.getMember('radius')
        self.thetamax = self.getMember('thetamax')

    def _initMembersDict(self):
        super(Cone,self)._initMembersDict()

        self._members['height']     = [float, 0.5]
        self._members['radius']     = [float, 0.5]
        self._members['thetamax']   = [float, 360.0]

    def render(self, ri, *args, **kwargs):
        ri.Cone(self.height, self.radius, self.thetamax)

def build(**kwargs):
    return Cone(**kwargs)
