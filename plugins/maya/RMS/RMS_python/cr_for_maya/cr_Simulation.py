import pymel.all as pm

import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node
from cr_RenderObject import CRRenderObject
from cr_DataObject import CRDataObject

from chronorender.finder import FinderFactory
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

    def createNode(self):
        return CRSimulation_Node()

    def export(self, md):
        sim = self._constructSim()
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        del sim

    def _import(self):
        sim = self._constructSim()
        sim.resolveAssets(FinderFactory().build('.'))
        lastframe = sim.getNumFrames()
        transforms = {}
        for frame in range(0, lastframe+1):
            curr_id = 0

            for robj in sim._robjs:
                data = sim._data.getData(frame, robj.condition)

                for entry in data:
                    if curr_id not in transforms:
                        transforms[curr_id] = pm.polyCube(n=self.node.name+str(frame))[0]

                    CRSimulation._setMayaTrans(transforms, curr_id, entry)
                    CRSimulation._setMayaRot(transforms, curr_id, entry)
                    curr_id += 1

            pm.setKeyframe(transforms.values(),at="translate",t=frame)
            pm.setKeyframe(transforms.values(),at="rotate",t=frame)
        del sim

    def _importRobjs(self, frame, transforms):
        curr_id = 0
        if curr_id not in transforms:
            transforms[curr_id] = pm.polyCube(n=self.node.name+str(i))[0]

        transforms[curr_id].translate.set(curr_trans[0],curr_trans[1],curr_trans[2])
        transforms[curr_id].rotate.set(rot[0],rot[1],rot[2])
        curr_id += 1

    @staticmethod
    def _setMayaTrans(transforms, curr_id, entry):
        curr_trans = [0.0, 0.0, 0.0]
        if 'pos_x'in entry:
            curr_trans[0] = entry['pos_x']
        if 'pos_y'in entry:
            curr_trans[0] = entry['pos_y']
        if 'pos_z'in entry:
            curr_trans[0] = entry['pos_z']
        transforms[curr_id].translate.set(curr_trans[0],
                curr_trans[1],curr_trans[2])

    @staticmethod
    def _setMayaRot(transforms, curr_id, entry):
        curr_rot = [0.0, 0.0, 0.0]
        if 'euler_x'in entry:
            curr_rot[0] = entry['euler_x']
        if 'euler_y'in entry:
            curr_rot[0] = entry['euler_y']
        if 'euler_z'in entry:
            curr_rot[0] = entry['euler_z']
        transforms[curr_id].rotate.set(curr_rot[0],
                curr_rot[1],curr_rot[2])

    def _constructSim(self):
        attrdict = self.attrs2Dict()
        simdict = attrdict[Simulation.getTypeName()]
        sim = self.sim_factories.build(Simulation.getTypeName(), **simdict)
        return sim

    def createFormGUI(self):
        win = super(CRSimulation, self).createFormGUI()
        self._createDataGUI()
        self._createRObjGUI()
        # self._createImportGUI()

    def _createDataGUI(self):
        pm.text( label='Data' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._dataTypeAttr,
                             ei=(0, DataObject.getTypeName()))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRDataObject,
                    self.datasrcs,
                    srcattr=CRSimulation_Node._dataTypeAttr))

    def _createRObjGUI(self):
        pm.text( label='RenderObject' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRSimulation_Node._robjTypeAttr,
                             ei=self._genEnumsFor(RenderObject))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRRenderObject,
                    self.robjs,
                    srcattr=CRSimulation_Node._robjTypeAttr))

    def _createImportGUI(self):
        pm.text( label='Import' ) 
        pm.text( label='This imports the entire simulation' ) 
        pm.button(label="Import", w=128,
                c=pm.Callback(self._import))
