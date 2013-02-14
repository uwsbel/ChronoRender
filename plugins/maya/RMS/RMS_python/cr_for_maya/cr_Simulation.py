import os, copy, string
import pymel.all as pm

import cr_GUI as gui
from cr_Object import CRObject
from cr_RenderObject import CRRenderObject

from chronorender.data import DataObject
from chronorender.datasource import DataSource
from chronorender.metadata import MDReaderFactory
from chronorender.renderobject import RenderObject
from chronorender.simulation import Simulation
from chronorender.cr_scriptable import Scriptable

class CRSimulation_Node(pm.nt.PolyCube):
    _handle = "simulation"
    _dataSrcTypeAttr = "src_type"
    _robjTypeAttr    = "robj_type"
    # _srcFactories = crinterface.Factories.getFactory(DataSource.getTypeName())

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute('simulation'):
                return True
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        if 'name' not in kwargs and 'n' not in kwargs:
            # kwargs['name'] = crinterface._simHandle
            kwargs['name'] = 'simulation'
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        # crinterface.addRootHandle(newNode)
        newNode.addAttr('chronorender', dt='string', h=True)
        newNode.addAttr('simulation', dt='string', h=True)

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

    def getShape(self):
        return self.getTransform().getShape()

    def getTransform(self):
        return self.listConnections()[0]

    def getPreShapeScript(self):
        return self.getShape().getAttr('rman__torattr___preShapeScript')

    def setPreShapeScript(self, script):
        return self.getShape().setAttr('rman__torattr___preShapeScript', script)

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
        self.robj_factories = self.factories.getFactory(RenderObject.getTypeName())
        self.numrobjs = 0

        pm.select(self.node)

    def export(self, md):
        attrdict = self.attrs2Dict()
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

        # robj = self.robj_factories.build(robjtype)
        # robj.name = 'robj'+str(self.numrobjs)
        # self.robjs.append(robj)
        robj = CRRenderObject(self.factories)
        # self.addCRObject(RenderObject, robj, prefix=robj.name)
        print "ADD NODE"
        self.addCRNode(robj)

        self.refreshGUI()
        # objname = CRSimulation_Node._robjprefix + str(CRSimulation_Node._numrobjs)
        # CRSimulation_Node._numrobjs += 1

        # robj = crrobj.build()
        # pm.parent(robj.name(), self.getShape().name())
        # self.addAttr(objname, at='message')
        # pm.mel.eval("connectAttr " + self.name() + '.' + objname + ' ' + robj.name() + '.parent')

        # self.refreshGUI()

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
        
def register():
    pm.factories.registerVirtualClass(CRSimulation_Node, nameRequired=False)

def build():
    register()
    crsim = CRSimulation_Node()
    crsim.init()

    return crsim

def main():
    register()
    build()
