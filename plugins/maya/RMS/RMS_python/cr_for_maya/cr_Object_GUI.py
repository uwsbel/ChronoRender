import pymel.all as pm
import cr_GUI as gui
import chronorender.cr_types as cr_types

class CRObject_GUI():
    def __init__(self, obj):
        self.obj = obj

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
        self.layout = pm.scrollLayout(cr=True)
        for obj_type, obj_vals in self.obj.attrs.iteritems():
            self._genMemberGUI(obj_type, obj_vals)

    # emit a GUI element for all objs that define this object
    def _genMemberGUI(self, obj_type, obj_vals):
        for inst_name, inst_vals in obj_vals[1].iteritems():
            self._genInstanceGUI(inst_name, inst_vals)
            pm.separator(height=10, style='double')

    # emit a GUI element for an object instance
    def _genInstanceGUI(self, inst_name, inst_vals):
        crobjs = []
        pm.text( label=inst_name) 
        for vals in inst_vals:
            attrname, typ, val, mem_name = vals[0], vals[1], vals[2], vals[3]
            if typ not in cr_types.builtins:
                crobjs.append(vals)
                continue

            self._genTypeGUI(attrname, typ, val)

        for vals in crobjs:
            attrname, typ, val, mem_name = vals[0], vals[1], vals[2], vals[3]
            if isinstance(val, list):
                if typ not in cr_types.builtins:
                    if self.obj._ignore(typ.getTypeName()): return
                    enum_attr = self.obj._getTypeEnumAttrName(typ)
                    pm.attrEnumOptionMenuGrp( l='Type',
                            at=self.obj.node.name()+'.'+enum_attr, ei=self.obj._genEnumsFor(typ))
                    pm.button(label="Add", w=64, c=pm.Callback(self.obj._addEnumeratedObject, typ, enum_attr))
            self._genInstanceGUI(mem_name, val)

    # emit a GUI element for specific types
    def _genTypeGUI(self, attrname, typ, val):
        if pm.attributeQuery(attrname, node=self.obj.node, h=True): return

        if typ == cr_types.url:
            pm.attrControlGrp(attribute=self.obj.node.name()+'.'+attrname)
            pm.button(label="Find", w=128, c=
                    pm.Callback(gui.setAttrFromFileDialog, self.obj.node,
                        attrname))
        else:
            pm.attrControlGrp(attribute=self.obj.node.name()+'.'+attrname)
