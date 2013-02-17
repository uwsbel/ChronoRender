import pymel.all as pm
import weakref

from cr_Object import CRObject, CRObject_Node
from cr_Geometry import CRGeometry
from cr_Shader import CRShader

from chronorender.geometry import Geometry
from chronorender.shader import Shader
from chronorender.renderobject import RenderObject

class CRRenderObject_Node(CRObject_Node):
    _handle = "robj"
    _geoTypeAttr = "geo_type"
    _sdrTypeAttr = "sdr_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        newNode.rename(cls._handle)

        CRRenderObject_Node.addAttrs(newNode)
        CRObject_Node.hideShape(newNode)

    @classmethod
    def addAttrs(cls, node):
        node.addAttr(CRRenderObject_Node._geoTypeAttr, dt='string', h=True)
        node.addAttr(CRRenderObject_Node._sdrTypeAttr, dt='string', h=True)

pm.factories.registerVirtualClass(CRRenderObject_Node, nameRequired=False)
        
class CRRenderObject(CRObject):
    crtype = RenderObject

    def __init__(self, factories, typename=''):
        super(CRRenderObject, self).__init__(factories, typename)
        self.crtype = RenderObject
        self.node = CRRenderObject_Node()
        self.robj_factories = self.factories.getFactory(RenderObject.getTypeName())

        self.geo_factories = self.factories.getFactory(Geometry.getTypeName())
        self.geo = weakref.WeakValueDictionary()
        self.numgeo = 0

        self.shdr_factories = self.factories.getFactory(Shader.getTypeName())
        self.shaders = weakref.WeakValueDictionary()
        self.numshaders = 0

        if not typename: typename = RenderObject.getTypeName()
        robj = self.robj_factories.build(typename)
        # self.addCRObject(RenderObject, robj, prefix='default')
        self.initMembers(RenderObject, robj, prefix='default')

        pm.select(self.node)

    def addShader(self):
        self.closeGUI()

    def createGUI(self):
        win = super(CRRenderObject, self).createGUI()
        layout = pm.scrollLayout('dataobj')
        pm.rowColumnLayout( numberOfColumns=3 )
        self._createRObjGUI()
        self._createShaderGUI()
        return win

    def _createRObjGUI(self):
        pm.text( label='Geometry' ) 
        pm.attrEnumOptionMenuGrp( l='Geo Type', 
                             at=self.node.name() +
                             '.'+CRRenderObject_Node._geoTypeAttr,
                             ei=self._genEnumsFor(Geometry))

        pm.button(label="Add Geometry", w=128,
                c=pm.Callback(self.addChildEnumCB, CRGeometry,
                    self.geo, name='geo', 
                    srcattr=CRRenderObject_Node._geoTypeAttr, 
                    counter=self.numgeo))

    def _createShaderGUI(self):
        pm.text( label='Shader' ) 
        pm.attrEnumOptionMenuGrp( l='Shader Type', 
                             at=self.node.name() +
                             '.'+CRRenderObject_Node._sdrTypeAttr,
                             ei=self._genEnumsFor(Shader))

        pm.button(label="Add Shader", w=128,
                c=pm.Callback(self.addChildEnumCB, CRShader,
                    self.shaders, name='shader', 
                    srcattr=CRRenderObject_Node._sdrTypeAttr, 
                    counter=self.numshaders))
