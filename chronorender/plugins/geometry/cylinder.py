from chronorender.geometry import Geometry

class Cylinder(Geometry):
    @staticmethod
    def getTypeName():
        return "cylinder"

    def __init__(self, *args, **kwargs):
        super(Cylinder,self).__init__(*args, **kwargs)

        self.radius = self.getMember('radius')
        self.height = self.getMember('height')
        # self.zmin = self.getMember('zmin') #zmax-zmin = heigh
        # self.zmax = self.getMember('zmax')
        self.thetamax = self.getMember('thetamax')

    def _initMembersDict(self):
        super(Cylinder,self)._initMembersDict()

        self._members['radius']     = [float, 1.0]
        self._members['height']     = [float, 1.0]
        # self._members['zmin']       = [float,-1.0]
        # self._members['zmax']       = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    # def updateMembers(self):
    #     self.setMember('radius', self.radius)
    #     self.setMember('thetamax', self.thetamax)
    #     self.setMember('zmin', self.zmin)
    #     self.setMember('zmax', self.zmax)

    def render(self, rib, *args, **kwargs):
        rib.Cylinder(self.radius, -self.height/2.0, self.height/2.0, self.thetamax, *args, **self._params)

def build(**kwargs):
    return Cylinder(**kwargs)
