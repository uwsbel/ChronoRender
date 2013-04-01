from chronorender.geometry import Geometry

class Disk(Geometry):
    @staticmethod
    def getTypeName():
        return "disk"

    def _initMembersDict(self):
        super(Disk,self)._initMembersDict()

        self.height = self.getVar('height')
        self.radius = self.getVar('radius')
        self.thetamax = self.getVar('thetamax')

    def _initMembersDict(self):
        super(Disk,self)._initMembersDict()

        self._members['height']     = [float, 0.0]
        self._members['radius']     = [float, 1.0]
        self._members['thetamax']   = [float, 360.0]

    def render(self, ri, *args, **kwargs):
        ri.Disk(self.height, self.radius, self.thetamax, *args, **kwargs)

def build(**kwargs):
    return Disk(**kwargs)
