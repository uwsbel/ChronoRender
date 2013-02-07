import pymel.all as pm
from chronorender.cr_object import Object

class CRInterface(pm.nt.PolyCube):
    _handle = "crHandle"

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute(CRInterface._handle):
                plug = fn.findPlug(CRInterface._handle)
                if plug.asString() == CRInterface._handle:
                    return True
                return False
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        newNode.addAttr(CRInterface._handle, dt='string', h=True)
        newNode.crHandle.set(CRInterface._handle)
        trans = newNode.listConnections()[0]
        trans.addAttr(CRInterface._handle, dt='string', h=True)
        trans.crHandle.set(CRInterface._handle)
        shape = trans.getShape()
        shape.addAttr(CRInterface._handle, dt='string', h=True)
        shape.crHandle.set(CRInterface._handle)

    @classmethod
    def addCRObjAttrs(cls, obj):
        for key, val in obj._members.iteritems():
            vtype = val[0]
            newNode.addAttr(key, dt='string')
            mtype = CRInterface.getMayaType(vtype)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        return

    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        return

    @classmethod
    def getMayaType(cls, vtype):
        if vtype == list:
            return 'float3'
        elif vtype == str:
            return 'string'
        else:
            return 'message'

    @staticmethod
    def getSelected(addt_attr=None):
        nodes = []
        selected = pm.selected()
        for node in selected:
            if not node.hasAttr('crHandle'):
                continue
            if addt_attr and not node.hasAttr(addt_attr):
                continue
            nodes.append(node)
        return nodes

    @staticmethod
    def getAll(addt_attr=None):
        nodes = []
        selected = pm.ls(typ='polyCube')
        for node in selected:
            if addt_attr and not node.hasAttr(addt_attr):
                continue
            nodes.append(node)
        return nodes

    def getShape(self):
        return self.getTransform().getShape()

    def getTransform(self):
        return self.listConnections()[0]

    def export(self):
        return

def register():
    pm.factories.registerVirtualClass(CRInterface, nameRequired=False)

def build():
    CRInterface()

def main():
    register()
    build()

def export():
    nodes = CRInterface.getAll()
    for node in nodes:
        node.export()
