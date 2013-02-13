import pymel.all as pm
import cr_Utils
import cr_GUI as gui
from chronorender.cr_object import Object
from chronorender.attribute import Attribute
from chronorender.option import Option
import chronorender.cr_types as cr_types

class CRObject(object):
    def __init__(self, factories):
        self.node       = pm.polyCube()
        self.factories  = factories
        self.window     = None
        self.attrs      = {}

    def export(self, md):
        return

    def createGUI(self):
        return pm.window()

    def refreshGUI(self):
        if not self.window: return
        pm.deleteUI(self.window)
        self.window = self.createGUI()
        pm.showWindow(self.window)

    def getConnectedNodes(self):
        out = [self.node.name()]
        for rel in self.node.listRelatives():
            if rel not in out:
                out.append(rel.name())
        for con in self.node.listConnections():
            if con not in out:
                out.append(con.name())

    def attrs2Dict(self):
        out = {}
        for obj_type, obj_vals in self.attrs.iteritems():
            out[obj_type] = self._getMemberDict(obj_vals)
        return out

    def _getMemberDict(self, obj_vals):
        out = []
        for inst_name, inst_vals in obj_vals[1].iteritems():
            out.append(self._getInstanceDict(inst_vals))
        return out

    def _getInstanceDict(self, inst_vals):
        out = {}
        for vals in inst_vals:
            attrname, typ, val, mem_name = vals[0], vals[1], vals[2], vals[3]
            if typ not in cr_types.builtins:
                val = self._getInstanceDict(val)
                out[mem_name] = val
                continue
            out[mem_name] = typ(self.node.getAttr(attrname))
        return out

    # add to attr dict {typname: {obj_name : [], obj2_name : []}}
    def addCRObject(self, typ, obj, prefix=''):
        if typ.getTypeName() not in self.attrs:
            self.attrs[typ.getTypeName()] = [0, {}]

        self.attrs[typ.getTypeName()][0] += 1
        obj_name = prefix + typ.getTypeName() + str(self.attrs[typ.getTypeName()][0])
        self.attrs[typ.getTypeName()][1][obj_name] = self._addMembersToNode(typ,obj,obj_name)

    # return list w/ [(attr1, typ, val), (attr2, type, val), ...]
    def _addMembersToNode(self, typ, obj, prefix=''):
        if self._ignore(typ.getTypeName()): return []
        if obj == None: obj = typ()

        out = []
        members = obj.getMembers()
        for mem_name, mem in members.iteritems():
            typ, val = mem[0], mem[1]
            out.extend(self._addAttr(mem_name, typ, val, prefix))
        return out

    # return [(attrname, typ, val, mem_name), ...]
    def _addAttr(self, mem_name, typ, val, prefix='', concrete=''):
        if val == None: val = typ()
        hidden = True if self._ignore(mem_name) else False
        attrname = CRObject._getAttrName(mem_name, prefix)
        mayatype = cr_Utils.crType2Maya(typ)

        if mayatype == 'string':
            self.node.addAttr(attrname, dt=mayatype, h=hidden, nn=mem_name)
            self.node.setAttr(attrname, str(val))
        elif typ not in cr_types.builtins:
            if self._ignore(typ.getTypeName()): return []
            if not concrete:
                concrete = typ.getTypeName()
                type_enum = self._getTypeEnumAttrName(typ)
                if self.node.hasAttr(type_enum):
                    concrete = self._getTypeFromEnum(typ, type_enum)
            val = self._addSubCRObject(typ, concrete, prefix)
        else:
            self.node.addAttr(attrname, at=mayatype, h=hidden, nn=mem_name)

        return [(attrname, typ, val, mem_name)]

    def _addSubCRObject(self, typ, concrete, prefix=''):
        obj = typ(factories=self.factories, type=concrete)
        prefix += typ.getTypeName()
        return self._addMembersToNode(typ, obj, prefix)

    def _removeAttr(self, obj, mem_name):
        if len(obj._members[mem_name]) > 0:
            obj._members[mem_name].pop()
        self.refreshGUI()

    # emit a GUI element for this object
    def generateAttrGUI(self):
        self.layout = pm.scrollLayout()
        for obj_type, obj_vals in self.attrs.iteritems():
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
                crobjs.append((mem_name,val))
                continue

            self._genTypeGUI(attrname, typ, val)

        for obj in crobjs:
            self._genInstanceGUI(obj[0], obj[1])

    # emit a GUI element for specific types
    def _genTypeGUI(self, attrname, typ, val):
        if pm.attributeQuery(attrname, node=self.node, h=True): return

        if typ == cr_types.url:
            pm.attrControlGrp(attribute=self.node.name()+'.'+attrname)
            pm.button(label="Find", w=128, c=
                    pm.Callback(gui.setAttrFromFileDialog, self.node,
                        attrname))
        else:
            pm.attrControlGrp(attribute=self.node.name()+'.'+attrname)

        if isinstance(val, list):
            if typ not in cr_types.builtins:
                if self._ignore(typ.getTypeName()): return
                pm.attrEnumOptionMenuGrp( l='Type', 
                                     at=self.node.name()+'.'+self._getTypeEnumAttrName(typ),
                                     ei=self._genEnumsFor(typ))
            # pm.button(label="Add", w=64, c=pm.Callback(self._addAttrGUI,
                # attrname, typ, val, prefix))

    def _addAttrGUI(self, name, typ, val, prefix='', concrete=''):
        self._addAttr(self, name, typ, val, prefix='', concrete='')
        self.refreshGUI()

    def _genEnumsFor(self, typ):
        enums = []
        factories = self.factories.getFactory(typ.getTypeName())
        classes = factories.getClasses()
        for i in range(0, len(classes)):
            en = (i, classes[i].getTypeName())
            enums.append(en)
        return enums

    def _getTypeEnumAttrName(self, typ):
        return typ.getTypeName() + '_type'

    def _getTypeFromEnum(self, typ, enum_attr):
        srctype = self.node.getAttr(enum_attr)
        srctype = 0.0 if not srctype else srctype
        return self._genEnumsFor(typ)[int(srctype)][1]

    def _ignore(self, name):
        if name == Attribute.getTypeName():
            return True
        if name == Option.getTypeName():
            return True
        if name == Object.getInstanceQualifier():
            return True
        return False

    @staticmethod
    def _getAttrName(name, prefix=''):
        return prefix + "_" + name if prefix else name
