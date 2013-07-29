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
        x = self.side
        y = self.side
        z = self.side
        points = [-x,-y,-z,
                x,-y,-z,
                -x,y,-z,
                x,y,-z,
                -x,-y,z,
                x,-y,z,
                -x,y,z,
                x,y,z]
        npolys = [4,4,4,4,4,4]
        nverticies = [0,2,3,1,0,1,5,4,0,4,6,2,1,3,7,5,2,6,7,3,4,5,7,6]
        # ri.SolidBegin("primitive")
        rib.PointsPolygons(npolys, nverticies, {"P":points})
        # # Bottom
        # rib.Polygon(P=[p,p,-p, -p,p,-p, -p,-p,-p, p,-p,-p])
        # #Top
        # rib.Polygon(P=[p,p,p, -p,p,p, -p,-p,p, p,-p,p])
        # #Near
        # rib.Polygon(P=[p,-p,p, -p,-p,p, -p,-p,-p, p,-p,-p])
        # #Far
        # rib.Polygon(P=[p,p,p, -p,p,p, -p,p,-p, p,p,-p])
        # #Right
        # rib.Polygon(P=[p,-p,p, p,p,p, p,p,-p, p,-p,-p])
        # #Left
        # rib.Polygon(P=[-p,-p,p, -p,p,p, -p,p,-p, -p,-p,-p])
        # ri.SolidEnd()



def build(**kwargs):
    return Cube(**kwargs)
