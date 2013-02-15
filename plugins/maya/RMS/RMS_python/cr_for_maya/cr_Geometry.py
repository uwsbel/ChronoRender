import pymel.all as pm
from cr_Object import CRObject, CRObject_Node
from chronorender.geometry import Geometry

class CRGeometry_Node(CRObject_Node):
    _handle = "geometry"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        name = newNode.rename('geo')
        CRObject_Node.hideShape(newNode)

pm.factories.registerVirtualClass(CRGeometry_Node, nameRequired=False)

class CRGeometry(CRObject):

    def __init__(self, factories, typename=''):
        super(CRGeometry, self).__init__(factories, typename)
        self.node = CRGeometry_Node()
        self.geo_factories = self.factories.getFactory(Geometry.getTypeName())

        if not typename: typename = Geometry.getTypeName()
        geo = self.geo_factories.build(typename)
        self.initMembers(Geometry, geo, prefix='default')

        pm.select(self.node)

    def export(self, md):
        attrdict = self.attrs2Dict()
        geodict = {Geometry.getTypeName() : attrdict}
        geo = self.geo_factories.build(Geometry.getTypeName(), **attrdict)
        md.addElement(Geometry.getTypeName(), geo.getSerialized())
        del geo

    def createGUI(self):
        return self.window
