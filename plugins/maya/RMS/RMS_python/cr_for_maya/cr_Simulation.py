import os, copy, string
import pymel.all as pm

import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node
from cr_RenderObject import CRRenderObject

from chronorender.data import DataObject
from chronorender.datasource import DataSource
from chronorender.metadata import MDReaderFactory
from chronorender.renderobject import RenderObject
from chronorender.simulation import Simulation
from chronorender.cr_scriptable import Scriptable

class CRSimulation_Node(CRObject_Node):
    _handle = "simulation"
    _dataSrcTypeAttr = "src_type"
    _robjTypeAttr    = "robj_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)

        trans = newNode.listConnections()[0]
        shape = trans.getShape()
        name = newNode.rename('sim')
        CRSimulation_Node.addAttrs(newNode, trans, shape)
        CRSimulation_Node.addRManAttrs(newNode, trans, shape)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        node.addAttr(CRSimulation_Node._dataSrcTypeAttr, dt='string', h=True)
        node.addAttr(CRSimulation_Node._robjTypeAttr, dt='string', h=True)

    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        pm.mel.eval('$attr = `rmanGetAttrName \"preShapeScript\"`;')
        melstr = 'rmanAddAttr ' + shape.name() + ' $attr \"cr_SimulationRI\";'
        pm.mel.eval(melstr)

pm.factories.registerVirtualClass(CRSimulation_Node, nameRequired=False)

class CRSimulation(CRObject):

    def __init__(self, factories):
        super(CRSimulation, self).__init__(factories)
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
        robjlist = []
        for robj in self.robjs:
            d = robj.attrs2Dict()[RenderObject.getTypeName()]
            robjlist.extend(d)
        attrdict[RenderObject.getTypeName()] = robjlist

        print attrdict
        simdict = {Simulation.getTypeName() : attrdict}
        sim = self.sim_factories.build(Simulation.getTypeName(), **attrdict)
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        del sim

    def addDataSource(self):
        self.numsrcs += 1
        srctype = self._getTypeFromEnum(DataSource,
                CRSimulation_Node._dataSrcTypeAttr)

        src = self.src_factories.build(srctype)
        src.name = 'src'+str(self.numsrcs)
        self.datasrcs.append(src)
        self.addCRObject(DataSource, src, prefix=src.name)

        self.refreshGUI()

    def addRenderObject(self):
        self.numrobjs += 1
        robjtype = self._getTypeFromEnum(RenderObject,
                CRSimulation_Node._robjTypeAttr)
        robj = CRRenderObject(self.factories)
        self.addCRNode(robj)
        self.robjs.append(robj)
        self.refreshGUI()

    def createGUI(self):
        form_name = self.node.name()+"_form"
        self.window = pm.window(height=512, menuBar=True)
        menu   = pm.menu(label='File', tearOff=True)
        layout = pm.scrollLayout(form_name)

        self._createDataSource_GUI()
        return self.window

    def _createDataSource_GUI(self):
        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Data Source' ) 

        pm.attrEnumOptionMenuGrp( l='Format', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._dataSrcTypeAttr,
                             ei=self._genEnumsFor(DataSource))

        pm.button(label="Add DataSource", w=128, c= lambda *args: self.addDataSource())
        pm.button(label="Add RenderObject", w=128, c= lambda *args:
                self.addRenderObject())
        self.generateAttrGUI()
