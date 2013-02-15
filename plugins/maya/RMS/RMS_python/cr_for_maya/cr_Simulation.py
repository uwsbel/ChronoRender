import pymel.all as pm

import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node
from cr_RenderObject import CRRenderObject
from cr_DataObject import CRDataObject

from chronorender.data import DataObject
from chronorender.datasource import DataSource
from chronorender.renderobject import RenderObject
from chronorender.simulation import Simulation
from chronorender.cr_scriptable import Scriptable

class CRSimulation_Node(CRObject_Node):
    _handle = "simulation"
    _robjTypeAttr = "robj_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)

        trans = newNode.listConnections()[0]
        shape = trans.getShape()
        name = newNode.rename(cls._handle)
        CRSimulation_Node.addAttrs(newNode, trans, shape)
        CRSimulation_Node.addRManAttrs(newNode, trans, shape)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        node.addAttr(CRSimulation_Node._robjTypeAttr, dt='string', h=True)

    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        pm.mel.eval('$attr = `rmanGetAttrName \"preShapeScript\"`;')
        melstr = 'rmanAddAttr ' + shape.name() + ' $attr \"cr_SimulationRI\";'
        pm.mel.eval(melstr)

pm.factories.registerVirtualClass(CRSimulation_Node, nameRequired=False)

class CRSimulation(CRObject):
    _nodes = []

    def __init__(self, factories, typename=''):
        super(CRSimulation, self).__init__(factories,typename)
        self.node = CRSimulation_Node()
        self.datasrcs = []
        self.sim_factories = self.factories.getFactory(Simulation.getTypeName())
        self.src_factories = self.factories.getFactory(DataSource.getTypeName())
        self.numsrcs = 0
        self.robjs = []
        self.numrobjs = 0

        pm.select(self.node)

    def export(self, md):
        attrdict = self.attrs2Dict()

        # srclist = []
        # for data in self.datasrcs:
            # srclist.append(data.attrs2Dict())
        if len(self.datasrcs) > 0:
            attrdict[DataObject.getTypeName()] = self.datasrcs[0].attrs2Dict()

        robjlist = []
        for robj in self.robjs:
            robjlist.append(robj.attrs2Dict())
        attrdict[RenderObject.getTypeName()] = robjlist

        sim = self.sim_factories.build(Simulation.getTypeName(), **attrdict)
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        del sim

    def addDataObject(self):
        self.numsrcs += 1
        src = CRDataObject(self.factories)
        src.rename('dataobj'+str(self.numsrcs))
        self.addCRNode(src)
        CRSimulation._nodes.append(src)
        self.datasrcs.append(src)
        self.closeGUI()

    def addRenderObject(self):
        self.numrobjs += 1
        robjtype = self._getTypeFromEnum(RenderObject,
                CRSimulation_Node._robjTypeAttr)
        robj = CRRenderObject(self.factories, robjtype)
        robj.rename('robj'+str(self.numrobjs))
        self.addCRNode(robj)
        CRSimulation._nodes.append(robj)
        self.robjs.append(robj)
        self.closeGUI()

    def createGUI(self):
        super(CRSimulation, self).createGUI()
        layout = pm.scrollLayout('sim')
        pm.separator(h=40, style='in')
        self._createDataGUI()
        pm.separator(h=40, style='in')
        self._createRObjGUI()
        # pm.separator(h=40, style='in')
        # self.generateAttrGUI()
        # pm.separator(h=40, style='in')
        # self.generateConnGUI()
        return self.window

    def _createDataGUI(self):
        # pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        # pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.rowColumnLayout( numberOfColumns=2 )
        pm.text( label='Data' ) 

        pm.button(label="Add", w=128, c= lambda *args:
                self.addDataObject())

    def _createRObjGUI(self):
        pm.rowColumnLayout( numberOfColumns=3 )
        pm.text( label='Render Object' ) 
        pm.attrEnumOptionMenuGrp( l='RObj Type', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._robjTypeAttr,
                             ei=self._genEnumsFor(RenderObject))

        pm.button(label="Add", w=128, c= lambda *args:
                self.addRenderObject())
