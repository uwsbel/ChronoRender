import pprint, inspect
import chronorender.factorydict as fd
from cr_types import floatlist, intlist, strlist

class ObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class Object(object):
    """
    base level object.  Parameterized by 
    """
    _pprinter = pprint.PrettyPrinter(indent=4)

    @staticmethod
    def getInstanceQualifier():
        return "type"

    @staticmethod
    def getTypeName():
        return "object"

    @staticmethod
    def _evalSerialParam(obj):
        if not obj:
            return None
        if hasattr(obj, 'getSerialized'):
            # out = obj.getSerialized()[obj.getBaseName()]
            out = obj.getSerialized()
            return out
        elif isinstance(obj, list):
            if len(obj) <= 0: return obj

            out = []
            for v in obj:
                val = Object._evalSerialParam(v)
                out.append(val)
            return out
        else:
            return str(obj)

    def getBaseName(self):
        return Object.getTypeName()

    def _buildFromFactory(self, basename, typename, **kwargs):
        fact = self._factories.getFactory(basename)
        return fact.build(typename, **kwargs)

    def __init__(self, factories=None, *args, **kwargs):
        self._members = {}
        self._params = {}
        self._factories = factories

        self._initMembersDict()
        self._initFromNamedArgs(kwargs)

    # override new to make Object a metacalls
    # return a concrete instance if factories are defined
    def __new__(cls, basename="", factories=None, recurse=False, *args, **kwargs):
        if factories and not recurse:
            if basename == "":
                basename = cls.getTypeName()

            # if type specified, create specific impl
            # else create base class
            typename = basename
            if Object.getInstanceQualifier() in kwargs:
                typename = kwargs[Object.getInstanceQualifier()]

            fact = factories.getFactory(basename)
            if fact:
                return fact.build(typename, factories=factories, recurse=True, **kwargs)

        return object.__new__(cls, *args, **kwargs)

    def __str__(self):
        return pprint.pformat(self.getSerialized())

    def _initMembersDict(self):
        self._members['recurse'] = [bool, False]
        self._members[Object.getInstanceQualifier()] = [str, type(self).getTypeName()]

    def _initFromNamedArgs(self, args):
        for key, val in args.iteritems():
            if key in self._members:
                vtype = self._members[key][0]

                out = self._evalParamType(vtype, val)
                if isinstance(self._members[key][1], list):
                    if isinstance(out, list):
                        if len(self._members[key][1]) > 0:
                            self._members[key][1] = out
                        else:
                            self._members[key][1].extend(out)
                    else:
                        self._members[key][1].append(out)
                else:
                    self._members[key][1] = out
            else:
                self._params[key] = val

    def _evalParamType(self, vtype, val):
        out = None
        if vtype == intlist or vtype == floatlist or vtype == strlist:
            out = vtype(val)
        elif isinstance(val, list):
            # out = []
            #out = [self._evalParamType(type(x), x) for x in val]
            out = [self._evalParamType(vtype, x) for x in val]
            # for elem in val:
                # out.append(self._evalParamType(vtype, elem))
        elif isinstance(val, dict):
            if self._factories and Object.getInstanceQualifier() in val:
                out = self._buildFromFactory(vtype.getTypeName(), 
                        val[Object.getInstanceQualifier()], **val)
            else:
                out = vtype(factories=self._factories, **val)
        else: 
            out = vtype(val)
        return out

    def getSerialized(self):
        self.updateMembers()
        objdict = {}
        for key, val in self._members.iteritems():
            if key == 'recurse' or key == 'basename':
                continue
            member = Object._evalSerialParam(val[1])
            if not member:
                continue
            objdict[key] = member
        for key, val in self._params.iteritems():
            param = Object._evalSerialParam(val)
            objdict[key] = param
        # return {self.getBaseName() : objdict}
        return objdict

    def getMember(self, name):
        if name in self._members:
            return self._members[name][1]
        elif name in self._params:
            return self._params[name]
        else:
            raise ObjectException('no member ' + name + ' in ' + str(type(self)))

    def setMember(self, name, val):
        if name in self._members:
            self._members[name][1] = val
        elif name in self._params:
            self._params[name] = val
        else:
            raise ObjectException('no member ' + name + ' in ' + str(type(self)))

    def updateMembers(self):
        return

    def addParameter(self, name, val):
        self._params[name] = val

    def getVar(self, varname, kwargs):
        if varname in kwargs:
            return kwargs[varname]
        else:
            return self.getMember(varname)

    def resolveAssets(self, assetman):
        self._resolvedAssetPaths = True
        return  []

    def setAsset(self, assetname, obj):
        return

