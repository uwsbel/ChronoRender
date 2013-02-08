import os
import pymel.all as pm
from cr_interface import CRInterface
from chronorender.data import DataObject
from chronorender.datasource import CSVDataSource
from chronorender.metadata import MDReaderFactory
from chronorender.simulation import Simulation

class CRSimulation(CRInterface):
    _handle = "simHandle"
    _numrobjs = 9

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute(CRSimulation._handle):
                return True
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRInterface._postCreateVirtual(newNode)

        trans = newNode.listConnections()[0]
        shape = trans.getShape()

        CRSimulation._addHandles(newNode, trans, shape)
        name = newNode.rename('sim')
        trans.rename(name+'_Transform')
        shape.rename(name+'_Shape')

        CRSimulation.addAttrs(newNode, trans, shape)
        CRSimulation.addRManAttrs(newNode, trans, shape)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        for i in range(0, CRSimulation._numrobjs):
            objname = 'robj_' + str(i)
            # shape.addAttr(objname, at='message')
            shape.addAttr(objname, dt='string')
            num = str(i) if i != 0 else ''
            shape.setAttr(objname, 'robj'+num)

        # shape.addAttr('scriptname', dt='string')
        # shape.addAttr('scriptfunc', dt='string')
        shape.addAttr('dataregex', dt='string')
        shape.setAttr('dataregex', 'C:\\Users\\Aaron\\Desktop\\ChronoRender\\chronorender\\test\\input\\data\\stationary\\*.dat')
        shape.addAttr('delim', dt='string')
        shape.setAttr('delim', ',')
        shape.addAttr('fields', dt='string')
        shape.setAttr('fields' , "[[\"id\", integer], [\"pos_x\", float], [\"pos_y\", float], [\"pos_z\", float], [\"euler_x\", float], [\"euler_y\", float], [\"euler_z\", float]]")


    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        pm.mel.eval('$attr = `rmanGetAttrName \"preShapeScript\"`;')
        melstr = 'rmanAddAttr ' + shape.name() + ' $attr \"cr_SimulationRI\";'
        pm.mel.eval(melstr)

    @classmethod
    def _addHandles(cls, node, trans, shape):
        node.addAttr(CRSimulation._handle, dt='string', h=True)
        trans.addAttr(CRSimulation._handle, dt='string', h=True)
        shape.addAttr(CRSimulation._handle, dt='string', h=True)

    def export(self):
        self.exportRObjs()
        path = self.getOutPathFor('root')
        path = os.path.join(path, self.name()+'.yml')
        if os.path.exists(path):
            os.remove(path)


        sim = self.createCRObject()
        md = MDReaderFactory.build(path)
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        md.writeToDisk()

        del sim
        del md

    def exportRObjs(self):
        nodes = self.getRObjs()
        for node in nodes:
            node.export()

    def getRObjs(self):
        out = []
        shape = self.getShape()
        for i in range(0, CRSimulation._numrobjs):
            objname = 'robj_' + str(i)
            robjname = shape.getAttr(objname)
            if not robjname:
                continue
            node = pm.ls(robjname)
            if node:
                out.extend(node)
        return out

    def createCRObject(self):
        shape = self.getShape()

        rsim = Simulation()

        nodes = self.getRObjs()
        for node in nodes:
            robj = node.createCRObject()
            rsim.addRenderObject(robj)

        datasrc = CSVDataSource(resource=str(shape.getAttr('dataregex')),
                delim=str(shape.getAttr('delim')),
                fields=[["id", "integer"], ["pos_z", "float"], ["pos_y", "float"], ["pos_x", "float"], ["euler_x", "float"], ["euler_y", "float"], ["euler_z", "float"]])
                # fields=shape.getAttr('fields'))
        data = DataObject()
        data.addDataSource(datasrc)
        rsim.setData(data)

        return rsim

def register():
    pm.factories.registerVirtualClass(CRSimulation, nameRequired=False)

def build():
    CRSimulation()

def main():
    register()
    build()

def export():
    nodes = CRInterface.getAll(CRSimulation._handle)
    for node in nodes:
        node.export()

def addDataField():
    nodes = CRInteface.getSelected(CRSimulation._handle)
    for node in nodes:
        shape = node.getShape()
