from chronorender.geometry import Geometry

class Box(Geometry):
    @staticmethod
    def getTypeName():
        return "box"

    def __init__(self, *args, **kwargs):
        super(Box,self).__init__(*args, **kwargs)

        # self.zmin = self.getMember('zmin') #zmax-zmin = heigh
        # self.zmax = self.getMember('zmax')
        self.x = self.getMember('xlength')
        self.y = self.getMember('ylength')
        self.z = self.getMember('zlength')

    def _initMembersDict(self):
        super(Box,self)._initMembersDict()

        self._members['xlength']          = [float, 1.0]
        self._members['ylength']          = [float, 1.0]
        self._members['zlength']          = [float, 1.0]
        # self._members['zmin']       = [float,-1.0]
        # self._members['zmax']       = [float, 1.0]

    # def updateMembers(self):
    #     self.setMember('radius', self.radius)
    #     self.setMember('thetamax', self.thetamax)
    #     self.setMember('zmin', self.zmin)
    #     self.setMember('zmax', self.zmax)

    def render(self, rib, *args, **kwargs):
        x = self.x
        y = self.y
        z = self.z
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

        # rib.SolidBegin("primitive")
        rib.PointsPolygons(npolys, nverticies, {"P":points})
        # # Bottom
        # rib.Polygon(P=[x,y,-z, -x,y,-z, -x,-y,-z, x,-y,-z])
        # #Top
        # rib.Polygon(P=[x,y,z, -x,y,z, -x,-y,z, x,-y,z])
        # #Near
        # rib.Polygon(P=[x,-y,z, -x,-y,z, -x,-y,-z, x,-y,-z])
        # #Far
        # rib.Polygon(P=[x,y,z, -x,y,z, -x,y,-z, x,y,-z])
        # #Right
        # rib.Polygon(P=[x,-y,z, x,y,z, x,y,-z, x,-y,-z])
        # #Left
        # rib.Polygon(P=[-x,-y,z, -x,y,z, -x,y,-z, -x,-y,-z])
        # rib.SolidEnd()


def build(**kwargs):
    return Box(**kwargs)
