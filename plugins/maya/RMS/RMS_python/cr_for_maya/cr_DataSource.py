import pymel.all as pm
from cr_Object import CRObject, CRObject_Node
from chronorender.datasource import DataSource

class CRDataSource_Node(CRObject_Node):
    _handle = "datasrc"

    @classmethod
    def _postCreateVirtual(cls, newNode):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        newNode.rename(cls._handle)
        CRObject_Node.hideShape(newNode)

pm.factories.registerVirtualClass(CRDataSource_Node, nameRequired=False)

class CRDataSource(CRObject):
    crtype = DataSource
    def __init__(self, factories, typename='', **kwargs):
        super(CRDataSource, self).__init__(factories, typename, **kwargs)

    def createNode(self):
        return CRDataSource_Node()
