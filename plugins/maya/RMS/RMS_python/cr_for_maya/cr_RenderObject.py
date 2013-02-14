import os
import pymel.all as pm

# import cr_Utils
import cr_GUI as gui
from cr_Object import CRObject

from chronorender.geometry import Archive, Geometry
from chronorender.shader import Shader
from chronorender.renderobject import RenderObject
from chronorender.cr_scriptable import Scriptable

# class CRRenderObject_Node(pm.nt.Mesh):
class CRRenderObject_Node(pm.nt.PolyCube):
    _handle = "robj"
    _counter = 0

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            return fn.hasAttribute(CRRenderObject_Node._handle)
        except: pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        if 'name' not in kwargs and 'n' not in kwargs:
            kwargs['name'] = CRRenderObject_Node._handle
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        newNode.addAttr('chronorender', dt='string', h=True)
        newNode.addAttr(CRRenderObject_Node._handle, dt='string', h=True)
        CRRenderObject_Node.addAttrs(newNode)

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

    def createCRObject(self):
        geo=Archive(filename=str(self.getAttr('rib_archive')))

        robj = RenderObject()
        robj.geometry = geo
        robj.condition = str(self.getAttr('condition'))
        rscript = self.getAttr('render_script')
        rfunc =self.getAttr('render_function')
        robj.script = Scriptable(
            file= str(rscript) if rscript else "",
            function= str(rfunc) if rfunc else "")

        return robj

    def attachRIBArchive(self, archive):
        pm.disconnectAttr(self.name() + '.rib_archive')
        pm.connectAttr(archive.name()+'.filename', self.name()+'.rib_archive')


    def attachMesh(self, mesh):
        # delete current connection
        # currmesh = crinterface.getMesh(self)
        # if currmesh:
            # pm.delete(currmesh.name())

        pm.disconnectAttr(self.name() + '.inMesh')
        pm.connectAttr(mesh.name()+'.outMesh', self.name()+'.inMesh')

    def attachShader(self, shader):
        return

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
        
# class CRRenderObject(CRObject):

    # def __init__(self, factories):
        # print "FACOREIS"
        # super(CRRenderObject, self).__init__(factories)
        # self.node = CRRenderObject_Node()
        # pm.select(self.node)
class CRRenderObject(CRObject):
    def __init__(self, factories):
        super(CRRenderObject, self).__init__(factories)

def register():
    pm.factories.registerVirtualClass(CRRenderObject, nameRequired=False)

def build():
    # register()
    robj = CRRenderObject()
    robj.init()
    return robj
