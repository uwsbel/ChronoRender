import pymel.all as pm

import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node

from chronorender.data import DataObject
from chronorender.datasource import DataSource
from chronorender.cr_scriptable import Scriptable

class CRDataObject_Node(CRObject_Node):
    _handle = "dataobject"
    _dataSrcTypeAttr = "src_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)

        trans = newNode.listConnections()[0]
        shape = trans.getShape()
        name = newNode.rename('data')
        CRDataObject_Node.addAttrs(newNode, trans, shape)
        CRObject_Node.hideShape(newNode)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        node.addAttr(CRDataObject_Node._dataSrcTypeAttr, dt='string', h=True)

pm.factories.registerVirtualClass(CRDataObject_Node, nameRequired=False)

class CRDataObject(CRObject):

    def __init__(self, factories, typename=''):
        super(CRDataObject, self).__init__(factories, typename)
        self.node = CRDataObject_Node()
        self.src_factories = self.factories.getFactory(DataSource.getTypeName())
        self.datasrcs = []
        self.numsrcs = 0

        pm.select(self.node)

    def export(self, md):
        attrdict = self.attrs2Dict()

    def addDataSource(self):
        self.numsrcs += 1
        srctype = self._getTypeFromEnum(DataSource,
                CRDataObject_Node._dataSrcTypeAttr)

        src = self.src_factories.build(srctype)
        src.name = 'src'+str(self.numsrcs)
        self.addCRObject(DataSource, src, prefix=src.name)
        self.datasrcs.append(src)

        self.refreshGUI()

    def createGUI(self):
        super(CRDataObject, self).createGUI()
        self._createDataSource_GUI()
        return self.window

    def _createDataSource_GUI(self):
        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Data Source' ) 

        pm.attrEnumOptionMenuGrp( l='Format', 
                             at=self.node.name() +
                             '.'+CRDataObject_Node._dataSrcTypeAttr,
                             ei=self._genEnumsFor(DataSource))

        pm.button(label="Add DataSource", w=128, c= lambda *args: self.addDataSource())
        self.gui.generateAttrGUI()
