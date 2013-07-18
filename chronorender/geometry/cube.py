from geometry import Geometry

class Cube(Geometry):
    @staticmethod
    def getTypeName():
        return "cube"

    def __init__(self, *args, **kwargs):
        super(Cube,self).__init__(*args, **kwargs)

        self.side = self.getMember('side')

    def __str__(self):
        return 'cube'

    def _initMembersDict(self):
        super(Cube, self)._initMembersDict()

        self._members['side'] = [float, 1.0]

    def updateMembers(self):
        self.setMember('side', self.side)

    def render(self, rib, *args, **kwargs):
        p = self.side
        ri.SolidBegin("primitive")
        # Bottom
        rib.Polygon(P=[p,p,-p, -p,p,-p, -p,-p,-p, p,-p,-p])
        #Top
        rib.Polygon(P=[p,p,p, -p,p,p, -p,-p,p, p,-p,p])
        #Near
        rib.Polygon(P=[p,-p,p, -p,-p,p, -p,-p,-p, p,-p,-p])
        #Far
        rib.Polygon(P=[p,p,p, -p,p,p, -p,p,-p, p,p,-p])
        #Right
        rib.Polygon(P=[p,-p,p, p,p,p, p,p,-p, p,-p,-p])
        #Left
        rib.Polygon(P=[-p,-p,p, -p,p,p, -p,p,-p, -p,-p,-p])
        ri.SolidEnd()



def build(**kwargs):
    return Cube(**kwargs)
