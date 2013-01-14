import pprint

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

    def __init__(self, *args, **kwargs):
        self._members = {}
        self._params = {}

        self._initMembersDict()
        self._initFromNamedArgs(kwargs)

    def __str__(self):
        return str(self._members) + str(self._params)

    def _initMembersDict(self):
        return

    def _initFromNamedArgs(self, args):
        for key, val in args.iteritems():
            if key in self._members:
                vtype = self._members[key][0]
                self._members[key][1] = self._evalParamType(vtype, val)
            else:
                self._params[key] = val

    def _evalParamType(self, vtype, val):
        out = None
        if vtype == 'collist':
            out = str.split(val, ":")
        elif vtype == 'spalist':
            out = str.split(val, ' ')
        elif vtype == 'comlist':
            out = str.split(val, ',')
        else: 
            out = vtype(val)
        return out

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

    def pprint(self):
        print 'Name: ' + self.getTypeName()
        print 'Data: '
        Object._pprinter.pprint(self._members)
        print 'Params: '
        Object._pprinter.pprint(self._params)


# extended object, can be rendered
class RenderableException(ObjectException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Renderable(Object):
    def __init__(self, *args, **kwargs):
        super(Renderable,self).__init__(*args, **kwargs)

        self._resolvedAssetPaths = False

    def __str__(self):
        return super(Renderable,self).__str__()

    def resolveAssets(self, searchpaths):
        self._resolvedAssetPaths = True
        return 

    def render(self, *args, **kwargs):
        return


# extended renderable, can have render scripted
class ScriptableException(RenderableException):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Scriptable(Renderable):
    def __init__(self, *args, **kwargs):
        super(Scriptable,self).__init__(*args, **kwargs)

    def __str__(self):
        return super(Scriptable,self).__str__()

    def render(self, *args, **kwargs):
        return
