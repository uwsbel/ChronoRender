from chronorender.geometry import Geometry

class Torus(Geometry):
    @staticmethod
    def getTypeName():
        return "torus"

    def __init__(self, *args, **kwargs):
        super(Torus,self).__init__(*args, **kwargs)

        self.thetamax = self.getMember('thetamax')
        self.major_radius = self.getMember('rmajor')
        self.minor_radius = self.getMember('rminor')
        self.phimin = self.getMember('phimin')
        self.phimax = self.getMember('phimax')

    def _initMembersDict(self):
        super(Torus,self)._initMembersDict()

        self._members['thetamax']   = [float, 360.0]
        self._members['rmajor']     = [float, 2.0]
        self._members['rminor']     = [float, 0.7]
        self._members['phimin']     = [float, 0.0]
        self._members['phimax']     = [float, 360.0]

    def render(self, ri, *args, **kwargs):
        ri.SolidBegin("primitive")
        ri.Torus(self.major_radius, self.minor_radius, self.phimin, self.phimax, 
                    self.thetamax, *args, **self._params)
        ri.SolidEnd()

def build(**kwargs):
    return Torus(**kwargs)
