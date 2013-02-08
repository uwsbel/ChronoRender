import os
import pymel.all as pm
from cr_interface import CRInterface
from chronorender.geometry import Archive
from chronorender.renderobject import RenderObject

class CRRenderObject(CRInterface):
    _handle = "robjHandle"

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute(CRRenderObject._handle):
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

        CRRenderObject._addHandles(newNode, trans, shape)
        name = newNode.rename('robj')
        trans.rename(name+'_Transform')
        shape.rename(name+'_Shape')

        CRRenderObject.addAttrs(newNode, trans, shape)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        shape.addAttr('name', dt='string')        
        shape.addAttr('condition', dt='string')        
        shape.setAttr('condition', 'id >= 0')
        shape.addAttr('rib_archive', dt='string')

    @classmethod
    def _addHandles(cls, node, trans, shape):
        node.addAttr(CRRenderObject._handle, dt='string', h=True)
        node.setAttr(CRRenderObject._handle, CRRenderObject._handle)
        trans.addAttr(CRRenderObject._handle, dt='string', h=True)
        trans.setAttr(CRRenderObject._handle, CRRenderObject._handle)
        shape.addAttr(CRRenderObject._handle, dt='string', h=True)
        shape.setAttr(CRRenderObject._handle, CRRenderObject._handle)

    def export(self):
        shape = self.getShape()
        pm.select(shape)
        self.createOutDirs()
        path = self.getOutPathFor('archive')
        path = os.path.join(path, shape.name())
        out = pm.exportSelected(path, type="RIB_Archive", shader=True)
        print out
        # self.getShape().setAttr('rib_archive', out)
        self.getShape().setAttr('rib_archive', shape.name())

    def createCRObject(self):
        shape = self.getShape()
        geo=Archive(filename=str(shape.getAttr('rib_archive')))

        robj = RenderObject()
        robj.geometry = geo
        robj.condition = str(shape.getAttr('condition'))
        return robj

def register():
    pm.factories.registerVirtualClass(CRRenderObject, nameRequired=False)

def build():
    CRRenderObject()

def main():
    register()
    build()

def export():
    nodes = CRInterface.getAll(CRRenderObject._handle)
    for node in nodes:
        node.export()
