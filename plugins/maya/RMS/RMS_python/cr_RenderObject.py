import os
import pymel.all as pm
import cr_interface as crinterface
from chronorender.geometry import Archive
from chronorender.renderobject import RenderObject
from chronorender.cr_scriptable import Scriptable

class CRRenderObject(pm.nt.Mesh):
# class CRRenderObject(pm.nt.PolyCube):
    _handle = "robj"
    _counter = 0

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            return fn.hasAttribute(CRRenderObject._handle)
        except: pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        if 'name' not in kwargs and 'n' not in kwargs:
            kwargs['name'] = CRRenderObject._handle
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        crinterface.addRootHandle(newNode)
        newNode.addAttr(CRRenderObject._handle, dt='string', h=True)
        CRRenderObject.addAttrs(newNode)

    @classmethod
    def addAttrs(cls, node):
        node.addAttr('parent', at='message')
        node.addAttr('name', dt='string')        
        node.addAttr('condition', dt='string')        
        node.setAttr('condition', 'id >= 0')
        node.addAttr('rib_archive', dt='string')
        node.addAttr('py_script', dt='string')
        node.addAttr('py_function', dt='string')

    def export(self, md):
        crinterface.createOutDirs()

        trans = self.getParent()
        x, y, z = trans.getAttr('translateX'), trans.getAttr('translateY'), trans.getAttr('translateZ')
        trans.setAttr('translateX', 0.0)
        trans.setAttr('translateY', 0.0)
        trans.setAttr('translateZ', 0.0)
        self.setAttr('primaryVisibility', True)
        self.setAttr('castsShadows', True)
        self.setAttr('receiveShadows', True)

        path = crinterface.getOutPathFor('archive')
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
        robj.script = Scriptable(
            scriptname=self.getAttr('py_script'),
            function=self.getAttr('py_function'))

        return robj

    def attachMesh(self, mesh):
        # delete current connection
        currmesh = crinterface.getMesh(self)
        if currmesh:
            pm.delete(currmesh.name())

        pm.disconnectAttr(self.name() + '.inMesh')
        pm.connectAttr(mesh.name()+'.outMesh', self.name()+'.inMesh')

    def attachShader(self, shader):
        return

    def init(self):
        cube = pm.polyCube()
        trans, mesh = cube[0], cube[1]
        self.attachMesh(trans.getShape())
        ptrans = self.getParent()
        ptrans.rename(CRRenderObject._handle+str(CRRenderObject._counter))
        self.rename(ptrans.name()+"Shape")

        self.setAttr('primaryVisibility', False)
        self.setAttr('castsShadows', False)
        self.setAttr('receiveShadows', False)

        pm.select(self)
        CRRenderObject._counter += 1

def register():
    pm.factories.registerVirtualClass(CRRenderObject, nameRequired=False)

def build():
    register()
    robj = CRRenderObject()
    robj.init()
    return robj
