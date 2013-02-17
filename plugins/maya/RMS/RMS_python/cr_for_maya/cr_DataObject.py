import pymel.all as pm
import weakref

import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node
from cr_DataSource import CRDataSource

from chronorender.data import DataObject
from chronorender.datasource import DataSource

class CRDataObject_Node(CRObject_Node):
    _handle = "dataobject"
    _dataSrcTypeAttr = "src_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        newNode.rename(cls._handle)
        CRDataObject_Node.addAttrs(newNode)
        CRObject_Node.hideShape(newNode)

    @classmethod
    def addAttrs(cls, node):
        node.addAttr(CRDataObject_Node._dataSrcTypeAttr, dt='string', h=True)

pm.factories.registerVirtualClass(CRDataObject_Node, nameRequired=False)

class CRDataObject(CRObject):
    crtype = DataObject

    def __init__(self, factories, typename=''):
        super(CRDataObject, self).__init__(factories, typename)
        self.crtype = DataObject
        self.node = CRDataObject_Node()
        self.src_factories = self.factories.getFactory(DataSource.getTypeName())
        self.datasrcs = weakref.WeakValueDictionary()
        self.numsrcs = 0

        pm.select(self.node)

    def createGUI(self):
        win = super(CRDataObject, self).createGUI()
        layout = pm.scrollLayout('dataobj')
        self._createDataSourceGUI()
        return win

    def _createDataSourceGUI(self):
        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Data Source' ) 

        pm.attrEnumOptionMenuGrp( l='Format', 
                             at=self.node.name() +
                             '.'+CRDataObject_Node._dataSrcTypeAttr,
                             ei=self._genEnumsFor(DataSource))

        pm.button(label="Add DataSource", w=128,
                c=pm.Callback(self.addChildEnumCB, CRDataSource,
                    self.datasrcs, name='src', 
                    srcattr=CRDataObject_Node._dataSrcTypeAttr, 
                    counter=self.numsrcs))
