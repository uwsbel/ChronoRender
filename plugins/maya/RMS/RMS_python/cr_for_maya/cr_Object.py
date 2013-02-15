import ast
import pymel.all as pm
import cr_Utils
import cr_GUI as gui
from chronorender.cr_object import Object
from chronorender.attribute import Attribute
from chronorender.option import Option
import chronorender.cr_types as cr_types

class CRObject_Node(pm.nt.PolyCube):
    _handle = "chronorender"
    _root = "cr"

    @classmethod
    def list(cls, *args, **kwargs):
        kwargs['type'] = cls.__melnode__
        return [node for node in pm.ls(*args, **kwargs) if isinstance(node, cls)]

    @classmethod
    def _isVirtual(cls, obj, name):
        fn = pm.api.MFnDependencyNode(obj)
        try:
            return fn.hasAttribute(cls._handle)
        except: pass
        return False

    @classmethod
    def _preCreateVirtual(cls, **kwargs ):
        if 'name' not in kwargs and 'n' not in kwargs:
            kwargs['name'] = cls._handle
        return kwargs

    @classmethod
    def _postCreateVirtual(cls, newNode ):
        newNode.addAttr(CRObject_Node._root, dt='string', h=True)
        shape = newNode.listConnections()[0].getShape()
        shape.setAttr('primaryVisibility', False)
        shape.setAttr('castsShadows', False)
        shape.setAttr('receiveShadows', False)

    def getShape(self):
        return self.getTransform().getShape()

    def getTransform(self):
        return self.listConnections()[0]

    def getPreShapeScript(self):
        return self.getShape().getAttr('rman__torattr___preShapeScript')

    def setPreShapeScript(self, script):
        return self.getShape().setAttr('rman__torattr___preShapeScript', script)

pm.factories.registerVirtualClass(CRObject_Node, nameRequired=False)


class CRObject(object):
    def __init__(self, factories, typename=''):
        self.node       = None
        self.factories  = factories
        self.window     = None
        self.attrs      = {}
        self.children   = {}
        self.parents    = {}

    def export(self, md):
        return

    def createGUI(self):
        form_name = self.node.name()+"_form"
        self.window = pm.window(height=512, menuBar=True)
        menu   = pm.menu(label='File', tearOff=True)
        return self.window

    def refreshGUI(self):
        if not self.window: return
        pm.deleteUI(self.window)
        self.window = self.createGUI()
        pm.showWindow(self.window)

    def closeGUI(self):
        if not self.window: return
        pm.deleteUI(self.window)

    def getConnectedNodes(self):
        out = [self.node.name()]
        for rel in self.node.listRelatives():
            if rel not in out:
                out.append(rel.name())
        for con in self.node.listConnections():
            if con not in out:
                out.append(con.name())

    def rename(self, name):
        self.node.rename(name)
        self.node.getShape().rename(name+'Shape')
        self.node.getTransform().rename(name+'Transform')

    def addRManAttrs(self):
        return

    #FIXME dear god this is terrible
    def attrs2Dict(self):
        out = {}
        for obj_type, obj_vals in self.attrs.iteritems():
            if isinstance(obj_vals, tuple):
                tmp = self._getInstanceDict([obj_vals])
                if obj_type in tmp:
                    out[obj_type] = tmp[obj_type]
            else:
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
                if self._ignore(typ.getTypeName()): continue
                val = self._getInstanceDict(val)
                out[mem_name] = val
                continue
            if isinstance(val, list):
                listval = self.node.getAttr(attrname)
                if listval:
                    out[mem_name] = ast.literal_eval(listval)
                else:
                    out[mem_name] = []
            else:
                if typ == cr_types.url:
                    typ = str
                out[mem_name] = typ(self.node.getAttr(attrname))
        return out

    def addCRNode(self, obj):
        node = obj.node
        pm.parent(node.getTransform().name(), self.node.getTransform().name())
        conn = self._getNodeConnectionAttr(obj)
        self.children[obj] = conn
        parent = obj.addParent(self)
        pm.mel.eval("connectAttr " + self.node.name()+ '.' + conn + ' ' +
                node.name() + '.' + parent)
        return conn

    def addParent(self, obj):
        conn = self._getNodeConnectionAttr(obj)
        self.parents[obj] = conn
        return conn

    def _getNodeConnectionAttr(self, obj):
        name = obj.node.name()
        if not self.node.hasAttr(name):
            self.node.addAttr(name, at='message')
        return name

    # add to attr dict {typname: {obj_name : [], obj2_name : []}}
    def addCRObject(self, typ, obj, prefix=''):
        if typ.getTypeName() not in self.attrs:
            self.attrs[typ.getTypeName()] = [0, {}]

        self.attrs[typ.getTypeName()][0] += 1
        obj_name = prefix + typ.getTypeName() + str(self.attrs[typ.getTypeName()][0])
        self.attrs[typ.getTypeName()][1][obj_name] = self.addMembersToNode(typ,obj,obj_name)

    def initMembers(self, typ, obj, prefix=''):
        attrs = self.addMembersToNode(typ,obj,prefix)
        for attr in attrs:
            attrname, typ, val, mem_name = attr[0], attr[1], attr[2], attr[3]
            self.attrs[mem_name] = attr

    # return list w/ [(attr1, typ, val), (attr2, type, val), ...]
    def addMembersToNode(self, typ, obj, prefix=''):
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
            self._addStringAttr(attrname, val, hidden, mem_name)
        elif typ not in cr_types.builtins:
            if not isinstance(val, list):
                val = self._addCRObjectAttr(typ, concrete, prefix)
                if not val: return []
        else:
            self.node.addAttr(attrname, at=mayatype, h=hidden, nn=mem_name)

        return [(attrname, typ, val, mem_name)]

    def _addStringAttr(self, attrname, val, hidden=False, nicename=''):
        if not nicename: nicename = attrname
        self.node.addAttr(attrname, dt='string', h=hidden, nn=nicename)
        self.node.setAttr(attrname, str(val))

    def _addCRObjectAttr(self, typ, concrete='', prefix=''):
        if self._ignore(typ.getTypeName()): return None
        if not concrete:
            concrete = typ.getTypeName()
            type_enum = self._getTypeEnumAttrName(typ)
            if self.node.hasAttr(type_enum):
                concrete = self._getTypeFromEnum(typ, type_enum)
        return self._addSubCRObject(typ, concrete, prefix)

    def _addSubCRObject(self, typ, concrete, prefix=''):
        obj = typ(factories=self.factories, type=concrete)
        prefix += typ.getTypeName()
        return self.addMembersToNode(typ, obj, prefix)

    def _removeAttr(self, obj, mem_name):
        if len(obj._members[mem_name]) > 0:
            obj._members[mem_name].pop()
        self.refreshGUI()

    def generateConnGUI(self):
        pm.columnLayout(nch=2)
        self.generateChildConnGUI()
        pm.separator()
        self.generateParentConnGUI()

    def generateChildConnGUI(self):
        pm.text(label='Children')
        for obj, name in self.children.iteritems():
            pm.text(label=name, align='left')

    def generateParentConnGUI(self):
        pm.text(label='Parents')
        for obj, name in self.parents.iteritems():
            pm.text(label=name, align='left')

    # emit a GUI element for this object
    def generateAttrGUI(self):
        self.layout = pm.scrollLayout(cr=True)
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
                crobjs.append(vals)
                continue

            self._genTypeGUI(attrname, typ, val)

        for vals in crobjs:
            attrname, typ, val, mem_name = vals[0], vals[1], vals[2], vals[3]
            if isinstance(val, list):
                if typ not in cr_types.builtins:
                    if self._ignore(typ.getTypeName()): return
                    enum_attr = self._getTypeEnumAttrName(typ)
                    pm.attrEnumOptionMenuGrp( l='Type', at=self.node.name()+'.'+enum_attr, ei=self._genEnumsFor(typ))
                    pm.button(label="Add", w=64, c=pm.Callback(self._addEnumeratedObject, typ, enum_attr))
            self._genInstanceGUI(mem_name, val)

    def _addEnumeratedObject(self, typ, enum_attr):
        fact = self.factories.getFactory(typ.getTypeName())
        srctype = self._getTypeFromEnum(typ, enum_attr)
        obj = fact.build(srctype)
        self.addCRObject(typ, obj)

        self.refreshGUI()

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

        # if isinstance(val, list):
            # pm.button(label="Add", w=64, c=pm.Callback(self._addAttrGUI,
                # attrname, typ, val, ''))

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
        name = typ.getTypeName() + '_type'
        if not self.node.hasAttr(name):
            self.node.addAttr(name, dt='string', h=True)
        return name

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
