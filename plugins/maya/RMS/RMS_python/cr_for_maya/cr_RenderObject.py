import os
import pymel.all as pm

import cr_Utils
import cr_GUI as gui
from cr_Object import CRObject, CRObject_Node

from chronorender.geometry import Archive, Geometry
from chronorender.shader import Shader
from chronorender.renderobject import RenderObject
from chronorender.cr_scriptable import Scriptable

# class CRRenderObject_Node(pm.nt.Mesh):
class CRRenderObject_Node(CRObject_Node):
    _handle = "robj"
    _counter = 0

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        CRObject_Node._postCreateVirtual(newNode)
        newNode.addAttr(cls._handle, dt='string', h=True)
        name = newNode.rename(cls._handle)

        # CRRenderObject_Node.addAttrs(newNode)

    @classmethod
    def addAttrs(cls, node):
        node.addAttr('parent', at='message')
        node.addAttr('name', dt='string')        
        node.addAttr('condition', dt='string')        
        node.setAttr('condition', 'id >= 0')
        node.addAttr('rib_archive', dt='string')
        node.addAttr('render_script', dt='string')
        node.addAttr('render_function', dt='string')

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
    def __init__(self, factories, typename=''):
        super(CRRenderObject, self).__init__(factories,typename)
        self.node = CRRenderObject_Node()
        self.robj_factories = self.factories.getFactory(RenderObject.getTypeName())

        print "TYPE", typename
        if not typename: typename = RenderObject.getTypeName()
        robj = self.robj_factories.build(typename)
        print "ROBJ", robj, robj.getSerialized(), robj._members
        self.addMembers(RenderObject, robj, prefix='default')

    def createGUI(self):
        form_name = self.node.name()+"_form"
        self.window = pm.window(menuBar=True)
        menu   = pm.menu(label='File', tearOff=True)
        layout = pm.scrollLayout(form_name)
        return self.window

