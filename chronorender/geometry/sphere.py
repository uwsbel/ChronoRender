# from chronorender.cr_object import Renderable

from geometry import Geometry

class Sphere(Geometry):
    @staticmethod
    def getTypeName():
        return "sphere"

    def __init__(self, *args, **kwargs):
        super(Sphere,self).__init__(*args, **kwargs)

        self.radius = self.getMember('radius')
        # self.zmin = self.getMember('zmin')
        # self.zmax = self.getMember('zmax')
        self.thetamax = self.getMember('thetamax')

    def __str__(self):
        return 'sphere'

    def _initMembersDict(self):
        super(Sphere,self)._initMembersDict()

        self._members['radius']     = [float, 1.0]
        # self._members['zmin']       = [float,-1.0]
        # self._members['zmax']       = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    def updateMembers(self):
        self.setMember('radius', self.radius)
        self.setMember('thetamax', self.thetamax)

    def render(self, rib, *args, **kwargs):
        rib.Sphere(self.radius, -self.radius, self.radius, self.thetamax)

def build(**kwargs):
    return Sphere(**kwargs)
