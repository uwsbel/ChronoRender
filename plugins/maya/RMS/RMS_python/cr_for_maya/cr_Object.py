import ast
import pymel.all as pm
import cr_Utils
from cr_for_maya.cr_Object_GUI import CRObject_GUI
from chronorender.cr_scriptable import Scriptable

from chronorender.cr_object import Object
from chronorender.attribute import Attribute
from chronorender.option import Option
import chronorender.cr_types as cr_types

class CRObject_Node(pm.nt.PolyCube):
    _handle = "chronorender"
    _root = "cr"
    _scriptTypeAttr = 'script_type'

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
        newNode.addAttr(CRObject_Node._scriptTypeAttr, dt='string', h=True)

    @classmethod
    def hideShape(cls, node):
        shape = node.listConnections()[0].getShape()
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
    crtype = Object
    _gNodes = []

    def __init__(self, factories, typename='', **kwargs):
        self.node       = self.createNode()
        self.factories  = factories
        self.type       = typename
        self.attrs      = {}
        self.children   = {}
        self.parents    = {}
        self.gui        = CRObject_GUI(self)
        self.bScript    = True

        clstypename = self.__class__.crtype.getTypeName()
        if not typename: typename = clstypename
        if Object.getInstanceQualifier() in kwargs:
            typename = kwargs[Object.getInstanceQualifier()]
        fact = self.factories.getFactory(clstypename)
        sim = fact.build(typename, **kwargs)
        self.initMembers(self.__class__.crtype, sim, prefix='default')

        self.rename(typename)
        CRObject.addObjToGlobalContext(self)

        pm.select(self.node)

    def createNode(self):
        return CRObject_Node()

    def export(self, md):
        return

    @staticmethod
    def addObjToGlobalContext(obj, weak_dict=None):
        CRObject._gNodes.append(obj)
        if weak_dict:
            weak_dict[id(obj)] = obj
        return obj

    def rename(self, name):
        newname = self.node.rename(name)
        self.node.getShape().rename(newname+'Shape')
        self.node.getTransform().rename(newname+'_t')

    def addRManAttrs(self):
        return

    def getCRType(self):
        return None

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
        for node in self.children:
            attrdict = node.attrs2Dict()
            typename = attrdict.keys()[0]
            vals = attrdict.values()[0]
            if typename not in out:
                out[typename] = vals
            else:
                if not isinstance(out[typename], list):
                    if len(out[typename]) > 0:
                        out[typename] = [out[typename]]
                    else:
                        out[typename] = []
                out[typename].append(vals)
        return {self.crtype.getTypeName(): out}

    def _getMemberDict(self, obj_vals):
        out = []
        for inst_name, inst_vals in obj_vals[1].iteritems():
            out.append(self._getInstanceDict(inst_vals))
        if len(out) == 1:
            return out[0]
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
                listval = None
                try:
                    listval = self.node.getAttr(attrname)
                    out[mem_name] = ast.literal_eval(listval)
                except Exception:
                    out[mem_name] = []
            else:
                if typ == cr_types.url:
                    typ = str
                try:
                    out[mem_name] = typ(self.node.getAttr(attrname))
                except Exception:
                    out[mem_name] = ''
        return out

    def addChildEnumCB(self, mayatype, objlist, 
            name='obj', srcattr=None, counter=None):
        srctype = mayatype.crtype.getTypeName()
        if srcattr:
            srctype = self._getTypeFromEnum(mayatype.crtype, srcattr)

        objname = name
        if counter:
            counter += 1
            objname = name+str(counter)

        src = mayatype(self.factories, srctype)
        src.rename(objname)
        self.addChild(src)
        CRObject.addObjToGlobalContext(src, objlist)
        self.closeGUI()
        pm.showWindow(src.createGUI())


    def addChild(self, obj):
        pm.parent(obj.node.getTransform().name(), self.node.getTransform().name())
        conn = self._addNode(self.children, obj)
        parent = obj.addParent(self)
        pm.mel.eval("connectAttr " + self.node.name()+ '.' + conn + ' ' +
                obj.node.name() + '.' + parent)
        return conn

    def removeChild(self, obj):
        self._removeNode(self.children, obj)

    def addParent(self, obj):
        return self._addNode(self.parents, obj)

    def removeParent(self, obj):
        self._removeNode(self.parents, obj)

    def _addNode(self, dic, obj):
        conn = self._getNodeConnectionAttr(obj)
        if not conn:
            conn = self._addNodeConnectionAttr(obj)
        dic[obj] = conn
        return conn

    def _removeNode(self, dic, obj):
        # if self._getNodeConnectionAttr(obj):
            # self._removeNodeConnectionAttr(obj)

        if obj in dic:
            del dic[obj]

    def _getNodeConnectionAttr(self, obj):
        name = obj.node.name()
        if self.node.hasAttr(name):
            return name
        return None

    def _addNodeConnectionAttr(self, obj):
        name = obj.node.name()
        if not self.node.hasAttr(name):
            self.node.addAttr(name, at='message')
        return name

    def _removeNodeConnectionAttr(self, obj):
        self.node.deleteAttr(obj.node.name())

    # add to attr dict {typname: {obj_name : [], obj2_name : []}}
    def addCRObject(self, typ, obj, prefix=''):
        if typ.getTypeName() not in self.attrs:
            self.attrs[typ.getTypeName()] = [0, {}]

        self.attrs[typ.getTypeName()][0] += 1
        obj_name = prefix + typ.getTypeName() + str(self.attrs[typ.getTypeName()][0])
        self.attrs[typ.getTypeName()][1][obj_name] = self.addMembersToNode(typ,obj,obj_name)

    def addScript(self, prefix=''):
        self.addCRObject(Scriptable, Scriptable(), prefix)
        self.bScript = False
        self.refreshGUI()

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

        if typ not in cr_types.builtins:
            return []
        elif mayatype == 'string':
            self._addStringAttr(attrname, val, hidden, mem_name)
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

    def _addEnumeratedObject(self, typ, enum_attr):
        fact = self.factories.getFactory(typ.getTypeName())
        srctype = self._getTypeFromEnum(typ, enum_attr)
        obj = fact.build(srctype)
        self.addCRObject(typ, obj)

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

    def createGUI(self):
        win = self.gui.createGUI()
        return win

    def createFormGUI(self):
        pass

    def _createAttrGUI(self):
        self.gui.generateAttrGUI()

    def _createScriptGUI(self):
        pm.text( label='Script' ) 

        pm.attrEnumOptionMenuGrp( l='Type', 
                at=self.node.name() +
                '.'+CRObject_Node._scriptTypeAttr,
                ei=(0, Scriptable.getTypeName()),
                en=self.bScript)

        pm.button(label="Add", w=128,
                c=pm.Callback(self.addScript, prefix='script'), 
                en=self.bScript)

    def refreshGUI(self):
        return self.gui.refreshGUI()

    def closeGUI(self):
        return self.gui.closeGUI()

    @staticmethod
    def _getAttrName(name, prefix=''):
        return prefix + "_" + name if prefix else name
