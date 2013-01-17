import pprint, inspect
import chronorender.factorydict as fd

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

    def _buildFromFactory(self, basename, typename, **kwargs):
        fact = self._factories.getFactory(basename)
        return fact.build(typename, **kwargs)

    def __init__(self, factories=None, *args, **kwargs):
        self._members = {}
        self._params = {}
        self._factories = factories

        self._initMembersDict()
        self._initFromNamedArgs(kwargs)

    def __str__(self):
        string = pprint.pformat(self._members)
        string += pprint.pformat(self._params)
        return string

    def _initMembersDict(self):
        return

    def _initFromNamedArgs(self, args):
        for key, val in args.iteritems():
            if key in self._members:
                vtype = self._members[key][0]

                out = self._evalParamType(vtype, val)
                if isinstance(self._members[key][1], list):
                    if isinstance(out, list):
                        self._members[key][1] += out
                    else:
                        self._members[key][1].append(out)
                else:
                    self._members[key][1] = out
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
        elif isinstance(val, list):
            out = []
            for elem in val:
                out.append(self._evalParamType(vtype, elem))
        elif isinstance(val, dict):
            if self._factories and Object.getInstanceQualifier() in val:
                out = self._buildFromFactory(vtype.getTypeName(), 
                        val[Object.getInstanceQualifier()], **val)
            else:
                out = vtype(factories=self._factories, **val)
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

    def getBaseClassTypeName(self):
        if isinstance(self, Object):
            return Object.getTypeName()
        return super(Object, self).getTypeName()

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

    def render(self, ri, *args, **kwargs):
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

    def render(self, ri, *args, **kwargs):
        # if script, run that
        return
