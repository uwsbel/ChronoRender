# from chronorender.cr_object import Renderable

from geometry import Geometry

class Sphere(Geometry):
    @staticmethod
    def getTypeName():
        return "sphere"

    def __init__(self, *args, **kwargs):
        super(Sphere,self).__init__(*args, **kwargs)

        self.radius = self.getMember('radius')
        self.zmin = self.getMember('zmin')
        self.zmax = self.getMember('zmax')
        self.thetamax = self.getMember('thetamax')

    def _initMembersDict(self):
        self._members['radius']     = [float, 1.0]
        self._members['zmin']       = [float,-1.0]
        self._members['zmax']       = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    def render(self, ri, *args, **kwargs):
        # ri.RiSphere(self.radius, self.zmin, self.zmax, self.thetamax)
        ri.RiSphere(self.radius, -self.radius, self.radius, self.thetamax)

def build(**kwargs):
    return Sphere(**kwargs)
