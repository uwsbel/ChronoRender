import os, copy, string
import pymel.all as pm

import cr_GUI as gui
import cr_interface as crinterface
import cr_RenderObject as crrobj

from chronorender.data import DataObject
from chronorender.datasource import CSVDataSource
from chronorender.metadata import MDReaderFactory
from chronorender.simulation import Simulation
from chronorender.cr_scriptable import Scriptable

class CRSimulation(pm.nt.PolyCube):
    _handle = "simulation"

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            if fn.hasAttribute(crinterface._simHandle):
                return True
        except:
            pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        if 'name' not in kwargs and 'n' not in kwargs:
            kwargs['name'] = crinterface._simHandle
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        crinterface.addRootHandle(newNode)
        newNode.addAttr(crinterface._simHandle, dt='string', h=True)

        trans = newNode.listConnections()[0]
        shape = trans.getShape()
        # trans.addAttr(crinterface._crHandle, dt='string', h=True)
        # shape.addAttr(crinterface._crHandle, dt='string', h=True)
        name = newNode.rename('sim')
        CRSimulation.addAttrs(newNode, trans, shape)
        CRSimulation.addRManAttrs(newNode, trans, shape)

    @classmethod
    def addAttrs(cls, node, trans, shape):
        node.addAttr('dataregex', dt='string')
        node.addAttr('delim', dt='string')
        node.setAttr('delim', ',')
        node.addAttr('py_script', dt='string')
        node.addAttr('py_function', dt='string')

        # shape.addAttr('scriptname', dt='string')
        # shape.addAttr('scriptfunc', dt='string')


    @classmethod
    def addRManAttrs(cls, node, trans, shape):
        pm.mel.eval('$attr = `rmanGetAttrName \"preShapeScript\"`;')
        melstr = 'rmanAddAttr ' + shape.name() + ' $attr \"cr_SimulationRI\";'
        pm.mel.eval(melstr)

    def getShape(self):
        return self.getTransform().getShape()

    def getTransform(self):
        return self.listConnections()[0]

    def getPreShapeScript(self):
        return self.getShape().getAttr('rman__torattr___preShapeScript')

    def setPreShapeScript(self, script):
        return self.getShape().setAttr('rman__torattr___preShapeScript', script)

    def export(self, md):
        sim = self.createCRObject()
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        del sim

    def createCRObject(self):
        rsim = Simulation()

        nodes = self.getAttrs(CRSimulation._robjprefix)
        for node in nodes:
            robj = node.createCRObject()
            rsim.addRenderObject(robj)

        datasrc = CSVDataSource(resource=str(self.getAttr('dataregex')),
                delim=str(self.getAttr('delim')),
                fields=self.getFields())
        script = self.getAttr('py_script')
        func =self.getAttr('py_function')
        robj.script = Scriptable(
            scriptname= str(script) if script else "",
            function= str(func) if func else "")
        datasrc.script = script

        data = DataObject()
        data.addDataSource(datasrc)
        rsim.setData(data)

        return rsim

    def setAttrFromFileDialog(self, attrname):
        text = pm.fileDialog()
        self.setAttr(attrname, text)

    def createGUI(self):
        form_name = self.name()+"_form"
        self.window = pm.window(height=512, menuBar=True)
        self.menu   = pm.menu(label='File', tearOff=True)
        self.layout = pm.scrollLayout(form_name)

        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Data Source' )
        # pm.rowColumnLayout( columnAlign=(5, 'left'), columnAttach=(5, 'left', 5), numberOfColumns=2 )
        pm.attrControlGrp(attribute=self.name()+'.dataregex')
        pm.button(label="Find", w=128, c= lambda *args: self.setAttrFromFileDialog('dataregex'))
        pm.attrControlGrp(attribute=self.name()+'.delim' )

        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Data Fields' )
        pm.button(label="Add DataElement", w=128, c= lambda *args: self.addDataElem())
        pm.rowColumnLayout( columnAttach=(5, 'left', 5), numberOfColumns=2, rowSpacing=(10,10), columnWidth=(250,124))
        elems = self.getAttrsByPrefix(CRSimulation._dataelemprefix)
        for dataelem in self.getAttrsByPrefix(CRSimulation._dataelemprefix):
            pm.attrControlGrp(attribute=self.name()+'.'+dataelem)
            pm.button(label="Remove", w=64, c=pm.Callback(self.removeDataElem, dataelem))
            # pm.textFieldButtonGrp(text=dataelem, editable=True, buttonLabel='Remove',
                    # buttonCommand = pm.Callback(self.removeDataElem, dataelem))

        pm.columnLayout( columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
        pm.text( label='Render Objects' )
        pm.button(label="Add Robj", w=64, c= lambda *args: self.addRObj())
        for robj in self.getAttrsByPrefix(CRSimulation._robjprefix):
            pm.textFieldButtonGrp(text=robj, editable=False, buttonLabel='Remove',
                    buttonCommand = pm.Callback(self.removeRObj, robj))

        return self.window

    def refreshGUI(self):
        if hasattr(self, 'window') and self.window:
            pm.deleteUI(self.window)
            self.window = self.createGUI()
            pm.showWindow(self.window)

    # ATTR STUFF###############################################3333
    def getAttrsByPrefix(self, prefix):
        out = []
        attrs = self.listAttr()
        for attr in attrs:
            toks = attr.split('.')
            attr = toks[len(toks)-1]
            if string.find(str(attr), prefix) == -1:
                continue
            if not self.getAttr(attr):
                self.deleteAttr(attr)
                continue
            out.append(attr)
        return out

    def getAttrs(self, prefix):
        attrs = self.getAttrsByPrefix(prefix)
        out = []
        for attr in attrs:
            objname = self.getAttr(attr)
            node = pm.ls(objname)
            if node:
                out.extend(node)
        return out

    # DATA STUFF###############################################3333
    _numdataelems = 0
    _dataelemprefix = "dataelem_"

    def addDataElem(self):
        elemname = CRSimulation._dataelemprefix +str(CRSimulation._numdataelems)
        CRSimulation._numdataelems += 1

        self.addAttr(elemname, dt='string')
        valstring = 'val_'+str(CRSimulation._numdataelems)+',float'
        self.setAttr(elemname, valstring)

        self.refreshGUI()

    def removeDataElem(self, name):
        elems = self.getAttrsByPrefix(CRSimulation._dataelemprefix)

        for elem in elems:
            if name != elem: continue
            self.deleteAttr(elem)
            self.refreshGUI()
            return

        self.refreshGUI()

    def getDataElems(self):
        return self.getAttrsByPrefix(CRSimulation._dataelemprefix)

    def getFields(self):
        attrs = self.getDataElems()
        out = []
        for attr in attrs:
            elem = self.getAttr(attr)
            toks = [str(x) for x in elem.split(',')]
            out.append(toks)
        return out

    # ROBJ STUFF###############################################3333
    _numrobjs = 0
    _robjprefix = "robj_"

    def addRObj(self):
        objname = CRSimulation._robjprefix + str(CRSimulation._numrobjs)
        CRSimulation._numrobjs += 1

        robj = crrobj.build()
        pm.parent(robj.name(), self.getShape().name())
        self.addAttr(objname, at='message')
        pm.mel.eval("connectAttr " + self.name() + '.' + objname + ' ' + robj.name() + '.parent')

        self.refreshGUI()

    def removeRObj(self, name):
        robjs = self.getAttrsByPrefix(CRSimulation._robjprefix)
        for robj in robjs:
            if name != robj:
                continue
            node = self.getAttr(robj)
            if node:
                pm.select(node, hi=True)
                mayanode = pm.selected()[0]
                pm.delete(pm.selected())
            self.deleteAttr(robj)
            self.refreshGUI()
            return

    def init(self):
        self.setAttr('dataregex', 'data/*.dat')
        self._initDataElems()

    def _initDataElems(self):
        numelems = 7
        for i in range(0, numelems):
            self.addDataElem()

        dataelems = self.getDataElems()
        for i in range(0, numelems):
            elem = dataelems[i]
            if i == 0:
                self.setAttr(elem, 'id,integer')
            elif i == 1:
                self.setAttr(elem, 'pos_x,float')
            elif i == 2:
                self.setAttr(elem, 'pos_y,float')
            elif i == 3:
                self.setAttr(elem, 'pos_z,float')
            elif i == 4:
                self.setAttr(elem, 'euler_x,float')
            elif i == 5:
                self.setAttr(elem, 'euler_y,float')
            elif i == 6:
                self.setAttr(elem, 'euler_z,float')

def register():
    pm.factories.registerVirtualClass(CRSimulation, nameRequired=False)

def build():
    register()
    crsim = CRSimulation()
    crsim.init()

    return crsim

def main():
    register()
    build()

def export():
    nodes = crinterface.getSelected(crinterface._simHandle)
    for node in nodes:
        node.export()
