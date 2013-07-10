from geometry import Geometry

class Cylinder(Geometry):
    @staticmethod
    def getTypeName():
        return "cylinder"

    def __init__(self, *args, **kwargs):
        import pdb; pdb.set_trace()
        super(Cylinder,self).__init__(*args, **kwargs)

        self.radius = self.getMember('radius')
        self.zmin = self.getMember('zmin') #zmax-zmin = height
        self.zmax = self.getMember('zmax')
        self.thetamax = self.getMember('thetamax')

    def _initMembersDict(self):
        super(Cylinder,self)._initMembersDict()

        self._members['radius']     = [float, 1.0]
        self._members['zmin']       = [float,-1.0]
        self._members['zmax']       = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    def updateMembers(self):
        self.setMember('radius', self.radius)
        self.setMember('thetamax', self.thetamax)
        self.setMember('zmin', self.zmin)
        self.setMember('zmax', self.zmax)

    def render(self, rib, *args, **kwargs):
        import pdb; pdb.set_trace()
        rib.Cylinder(self.radius, self.zmin, self.zmax, self.thetamax)

def build(**kwargs):
    return Cylinder(**kwargs)
