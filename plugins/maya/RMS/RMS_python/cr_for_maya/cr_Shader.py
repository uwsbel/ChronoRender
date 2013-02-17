import pymel.all as pm
from cr_Object import CRObject, CRObject_Node
from chronorender.shader import Shader

class CRShader_Node(CRObject_Node):
    _handle = "shader"

    @classmethod
    def _postCreateVirtual(cls, newNode):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        newNode.rename('shader')
        CRObject_Node.hideShape(newNode)

pm.factories.registerVirtualClass(CRShader_Node, nameRequired=False)

class CRShader(CRObject):
    crtype = Shader

    def __init__(self, factories, typename=''):
        super(CRShader, self).__init__(factories, typename)
        self.node = CRShader_Node()
        self.sdr_factories = self.factories.getFactory(Shader.getTypeName())

        if not typename: 
            typename = Shader.getTypeName()
        sdr = self.sdr_factories.build(typename)
        self.initMembers(Shader, sdr, prefix='default')

        pm.select(self.node)
