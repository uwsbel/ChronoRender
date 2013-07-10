from chronorender.geometry import Geometry

class Ellipsoid(Geometry):
    @staticmethod
    def getTypeName():
        return "ellipsoid"

    def __init__(self, *args, **kwargs):
        super(Ellipsoid,self).__init__(*args, **kwargs)

        self.radius = self.getMember('radius')
        # self.zmin = self.getMember('zmin') #zmax-zmin = heigh
        # self.zmax = self.getMember('zmax')
        self.thetamax = self.getMember('thetamax')

    def _initMembersDict(self):
        super(Ellipsoid,self)._initMembersDict()

        self._members['radius']     = [float, 1.0]
        # self._members['zmin']       = [float,-1.0]
        # self._members['zmax']       = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    # def updateMembers(self):
    #     self.setMember('radius', self.radius)
    #     self.setMember('thetamax', self.thetamax)
    #     self.setMember('zmin', self.zmin)
    #     self.setMember('zmax', self.zmax)

    def render(self, rib, *args, **kwargs):
        rib.Scale(1, 0.1, 1)
        rib.Sphere(self.radius, -self.radius, self.radius, self.thetamax)

def build(**kwargs):
    return Ellipsoid(**kwargs)
