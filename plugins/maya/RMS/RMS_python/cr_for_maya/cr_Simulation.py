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

import weakref

class CRSimulation_Node(CRObject_Node):
    _handle = "simulation"
    _robjTypeAttr = "robj_type"
    _dataTypeAttr = "data_type"

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
        node.addAttr(CRSimulation_Node._dataTypeAttr, dt='string', h=True)

    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        pm.mel.eval('$attr = `rmanGetAttrName \"preShapeScript\"`;')
        melstr = 'rmanAddAttr ' + shape.name() + ' $attr \"cr_SimulationRI\";'
        pm.mel.eval(melstr)

pm.factories.registerVirtualClass(CRSimulation_Node, nameRequired=False)

class CRSimulation(CRObject):
    crtype = Simulation

    def __init__(self, factories, typename='', **kwargs):
        super(CRSimulation, self).__init__(factories, typename, **kwargs)

        self.sim_factories = self.factories.getFactory(Simulation.getTypeName())
        self.datasrcs = weakref.WeakValueDictionary()
        self.robjs = weakref.WeakValueDictionary()
        self.numsrcs = 0
        self.numrobjs = 0

    def createNode(self):
        return CRSimulation_Node()

    def export(self, md):
        attrdict = self.attrs2Dict()
        simdict = attrdict[Simulation.getTypeName()]
        sim = self.sim_factories.build(Simulation.getTypeName(), **simdict)
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        del sim

    def createFormGUI(self):
        win = super(CRSimulation, self).createFormGUI()
        self._createDataGUI()
        self._createRObjGUI()

    def _createDataGUI(self):
        pm.text( label='Data' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._dataTypeAttr,
                             ei=(0, DataObject.getTypeName()))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRDataObject,
                    self.datasrcs, name='data', 
                    srcattr=CRSimulation_Node._dataTypeAttr, 
                    counter=self.numsrcs))

    def _createRObjGUI(self):
        pm.text( label='RenderObject' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._robjTypeAttr,
                             ei=self._genEnumsFor(RenderObject))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRRenderObject,
                    self.robjs, name='robj', 
                    srcattr=CRSimulation_Node._robjTypeAttr, 
                    counter=self.numrobjs))
