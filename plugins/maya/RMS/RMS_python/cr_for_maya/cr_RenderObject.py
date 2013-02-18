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

    def __init__(self, factories, typename='', **kwargs):
        super(CRRenderObject, self).__init__(factories, typename, **kwargs)
        self.geo = weakref.WeakValueDictionary()
        self.shaders = weakref.WeakValueDictionary()

    def createNode(self):
        return CRRenderObject_Node()

    def createFormGUI(self):
        win = super(CRRenderObject, self).createFormGUI()
        self._createRObjGUI()
        self._createShaderGUI()

    def _createRObjGUI(self):
        pm.text( label='Geometry' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRRenderObject_Node._geoTypeAttr,
                             ei=self._genEnumsFor(Geometry))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRGeometry,
                    self.geo,
                    srcattr=CRRenderObject_Node._geoTypeAttr))

    def _createShaderGUI(self):
        pm.text( label='Shader' ) 
        pm.attrEnumOptionMenuGrp( l='Type', 
                             at=self.node.name() +
                             '.'+CRRenderObject_Node._sdrTypeAttr,
                             ei=self._genEnumsFor(Shader))

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addChildEnumCB, CRShader,
                    self.shaders,
                    srcattr=CRRenderObject_Node._sdrTypeAttr))
 # 6 %DATA_FORMAT=tt,lx,ly,lz,bx,by,bz,r0,r1,r2,r3,ax,ay,az,vx,vy,vz,e0,e1,e2,e3
[['tt','integer'],['lx','integer'],['ly','integer'],['lz','integer'],['bx','float'],['by','float'],['bz','float'],['r0','float'],['r1','float'],['r2','float'],['r3','float'],['pos_x','float'],['pos_y','float'],['pos_z','float'],['vx','float'],['vy','float'],['vz','float'],['euler_x','float'],['euler_y','float'],['euler_z','float'],['e3','float']]
