import pymel.all as pm
import cr_GUI as gui
import chronorender.cr_types as cr_types

class CRObject_GUI():
    def __init__(self, obj):
        self.obj = obj
        self.window     = None

    def createGUI(self):
        self.window = pm.window(menuBar=True)
        menu   = pm.menu(label='File', tearOff=True)
        pm.rowColumnLayout( numberOfColumns=3 )
        self.obj.createFormGUI()
        self.obj._createAttrGUI()
        self.obj._createScriptGUI()
        return self.window

    def refreshGUI(self):
        if not self.window: return
        pm.deleteUI(self.window)
        self.window = self.createGUI()
        pm.showWindow(self.window)

    def closeGUI(self):
        if not self.window: return
        pm.deleteUI(self.window)

    def generateConnGUI(self):
        pm.columnLayout(nch=2)
        self.generateChildConnGUI()
        pm.separator()
        self.generateParentConnGUI()

    def generateChildConnGUI(self):
        pm.text(label='Children')
        for obj, name in self.obj.children.iteritems():
            pm.text(label=name, align='left')

    def generateParentConnGUI(self):
        pm.text(label='Parents')
        for obj, name in self.obj.parents.iteritems():
            pm.text(label=name, align='left')

    # emit a GUI element for this object
    def generateAttrGUI(self):
        for inst_name, inst_vals in self.obj.attrs.iteritems():
            if isinstance(inst_vals, list):
                self._genInstanceGUI(inst_vals[0], inst_vals[1])
            else:
                attrname, typ, val, mem_name = inst_vals[0], inst_vals[1], inst_vals[2], inst_vals[3]
                if typ not in cr_types.builtins: continue

                self._genTypeGUI(attrname, typ, val)

    # emit a GUI element for an object instance
    def _genInstanceGUI(self, inst_name, inst_vals):
        for vals in inst_vals:
            attrname, typ, val, mem_name = vals[0], vals[1], vals[2], vals[3]
            if typ not in cr_types.builtins: continue
            self._genTypeGUI(attrname, typ, val)

    # emit a GUI element for specific types
    def _genTypeGUI(self, attrname, typ, val):
        if pm.attributeQuery(attrname, node=self.obj.node, h=True): return

        pm.text(l='Attribute')
        if typ == cr_types.url:
            pm.attrControlGrp(attribute=self.obj.node.name()+'.'+attrname)
            pm.button(label="Find", w=128, c=
                    pm.Callback(gui.setAttrFromFileDialog, self.obj.node,
                        attrname))
        else:
            pm.attrControlGrp(attribute=self.obj.node.name()+'.'+attrname)
            pm.button(label="Ignore", w=128, en=False)
