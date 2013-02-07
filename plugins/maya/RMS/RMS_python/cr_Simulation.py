import pymel.all as pm
from cr_interface import CRInterface
from chronorender.simulation import Simulation

class CRSimulation(CRInterface):
    _handle = "simHandle"

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
        shape.addAttr('dataregex', dt='string')
        shape.addAttr('fields', dt='string')
        shape.addAttr('delim', dt='string')

        for i in range(0, 9):
            objname = 'robj_' + str(i)
            shape.addAttr(objname, at='message')

        shape.addAttr('scriptname', dt='string')
        shape.addAttr('scriptfunc', dt='string')

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

    @classmethod
    def export(cls):
        print "GORB"

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
