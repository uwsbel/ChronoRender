import os
import pymel.all as pm

import cr_Utils
from cr_Object import CRObject, CRObject_Node
from cr_Geometry import CRGeometry

from chronorender.geometry import Geometry
from chronorender.shader import Shader
from chronorender.renderobject import RenderObject

# class CRRenderObject_Node(pm.nt.Mesh):
class CRRenderObject_Node(CRObject_Node):
    _handle = "robj"
    _counter = 0
    _geoTypeAttr = "geo_type"

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        name = newNode.rename(cls._handle)

        CRRenderObject_Node.addAttrs(newNode)
        CRObject_Node.hideShape(newNode)

    @classmethod
    def addAttrs(cls, node):
        node.addAttr(CRRenderObject_Node._geoTypeAttr, dt='string', h=True)
        # node.addAttr('parent', at='message')
        # node.addAttr('name', dt='string')        
        # node.addAttr('condition', dt='string')        
        # node.setAttr('condition', 'id >= 0')
        # node.addAttr('rib_archive', dt='string')
        # node.addAttr('render_script', dt='string')
        # node.addAttr('render_function', dt='string')

    def export(self, md):
        trans = self.getParent()
        x, y, z = trans.getAttr('translateX'), trans.getAttr('translateY'), trans.getAttr('translateZ')
        trans.setAttr('translateX', 0.0)
        trans.setAttr('translateY', 0.0)
        trans.setAttr('translateZ', 0.0)
        self.setAttr('primaryVisibility', True)
        self.setAttr('castsShadows', True)
        self.setAttr('receiveShadows', True)

        path = cr_Utils.getOutPathFor('archive')
        path = os.path.join(path, self.name())
        pm.select(self)

        # option string for exporting only single RIB Archive
        out = pm.exportSelected(path, type="RIB_Archive", shader=True, force=True, options="rmanExportRIBCompression=0;rmanExportFullPaths=1;rmanExportGlobalLights=0;rmanExportLocalLights=0;rmanExportCoordinateSystems=0;rmanExportShaders=0;rmanExportAttributeBlock=0;rmanExportMultipleFrames=0;rmanExportStartFrame=1;rmanExportEndFrame=10;rmanExportByFrame=1")
        out = os.path.relpath(out)       
        out = out.replace('\\', '/')

        self.setAttr('rib_archive', out)
        trans.setAttr('translateX', x)
        trans.setAttr('translateY', y)
        trans.setAttr('translateZ', z)
        self.setAttr('castsShadows', False)
        self.setAttr('primaryVisibility', False)
        self.setAttr('receiveShadows', False)

    def attachRIBArchive(self, archive):
        pm.disconnectAttr(self.name() + '.rib_archive')
        pm.connectAttr(archive.name()+'.filename', self.name()+'.rib_archive')

    def attachMesh(self, mesh):
        pm.disconnectAttr(self.name() + '.inMesh')
        pm.connectAttr(mesh.name()+'.outMesh', self.name()+'.inMesh')

    def init(self):
        cube = pm.polyCube()
        trans, mesh = cube[0], cube[1]
        self.attachMesh(trans.getShape())
        ptrans = self.getParent()
        ptrans.rename(CRRenderObject_Node._handle+str(CRRenderObject_Node._counter))
        self.rename(ptrans.name()+"Shape")

        self.setAttr('primaryVisibility', False)
        self.setAttr('castsShadows', False)
        self.setAttr('receiveShadows', False)

        pm.select(self)
        CRRenderObject_Node._counter += 1

pm.factories.registerVirtualClass(CRRenderObject_Node, nameRequired=False)
        
class CRRenderObject(CRObject):
    _nodes = []

    def __init__(self, factories, typename=''):
        super(CRRenderObject, self).__init__(factories,typename)
        self.node = CRRenderObject_Node()
        self.robj_factories = self.factories.getFactory(RenderObject.getTypeName())

        self.numgeo = 0
        self.geo_factories = self.factories.getFactory(Geometry.getTypeName())
        self.geo = []

        self.numshaders = 0
        self.shdr_factories = self.factories.getFactory(Shader.getTypeName())
        self.shaders = []

        if not typename: typename = RenderObject.getTypeName()
        robj = self.robj_factories.build(typename)
        self.initMembers(RenderObject, robj, prefix='default')

    def attrs2Dict(self):
        attrdict = super(CRRenderObject, self).attrs2Dict()
        attrdict[Geometry.getTypeName()] = [geo.attrs2Dict() for geo in self.geo]
        return attrdict

    def export(self, md):
        attrdict = self.attrs2Dict()
        # attrdict[RenderObject.getTypeName()] = [geo.attrs2Dict() for geo in self.geo]
        geolist = []
        for geo in self.geo:
            geolist.append(geo.attrs2Dict())
        attrdict[Shader.getTypeName()] = geolist
        # attrdict[Shader.getTypeName()] = [shader.attrs2Dict() for shader in self.shaders]
        robj = self.robj_factories.build(RenderObject.getTypeName(), **attrdict)
        md.addElement(RenderObject.getTypeName(),  robj.getSerialized())
        del robj

    def addGeometry(self):
        self.numgeo += 1
        geotype = self._getTypeFromEnum(Geometry,
                CRRenderObject_Node._geoTypeAttr)
        src = CRGeometry(self.factories, geotype)
        src.rename('geo'+str(self.numgeo))
        self.addCRNode(src)
        CRRenderObject._nodes.append(src)
        self.geo.append(src)
        self.closeGUI()

    def addShader(self):
        self.closeGUI()

    def createGUI(self):
        form_name = self.node.name()+"_form"
        self.window = pm.window(menuBar=True)
        menu   = pm.menu(label='File', tearOff=True)
        layout = pm.scrollLayout(form_name)
        self._createRObjGUI()
        self._createShaderGUI()
        return self.window

    def _createRObjGUI(self):
        pm.rowColumnLayout( numberOfColumns=3 )
        pm.text( label='Geometry' ) 
        pm.attrEnumOptionMenuGrp( l='Geo Type', 
                             at=self.node.name() +
                             '.'+CRRenderObject_Node._geoTypeAttr,
                             ei=self._genEnumsFor(Geometry))

        pm.button(label="Add", w=128, c= lambda *args:
                self.addGeometry())

    def _createShaderGUI(self):
        pm.rowColumnLayout( numberOfColumns=2 )
        pm.text( label='Shader' ) 
        pm.button(label="Add", w=128, c= lambda *args:
                self.addShader())
