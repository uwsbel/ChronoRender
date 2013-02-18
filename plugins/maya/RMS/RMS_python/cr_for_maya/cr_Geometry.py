import pymel.all as pm
from cr_Object import CRObject, CRObject_Node
from chronorender.geometry import Geometry

class CRGeometry_Node(CRObject_Node):
    _handle = "geometry"

    @classmethod
    def _postCreateVirtual(cls, newNode):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        newNode.rename(cls._handle)
        CRObject_Node.hideShape(newNode)

pm.factories.registerVirtualClass(CRGeometry_Node, nameRequired=False)

class CRGeometry(CRObject):
    crtype = Geometry

    def __init__(self, factories, typename='', **kwargs):
        super(CRGeometry, self).__init__(factories, typename, **kwargs)

    def createNode(self):
        return CRGeometry_Node()
