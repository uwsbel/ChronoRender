import xml.etree.ElementTree as ET
from itertools import groupby

class MetaDataException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MetaData():
    @staticmethod
    def _convertXMLToDict(parent):
        # ret = {}
        # if parent.items(): ret.update(dict(parent.items()))
        # if parent.text: ret['__content__'] = parent.text
        # if ('List' in parent.tag):
            # ret['__list__'] = []
            # for elem in parent:
                # ret['__list__'].append(MetaData._convertXMLToDict(elem))
        # else:
            # for elem in parent:
                # ret[elem.tag] = MetaData._convertXMLToDict(elem)
        # return ret
        def _xml2d(e):
            kids = dict(e.attrib)
            if e.text:
                kids['__content__'] = e.text
            if e.tail:
                kids['__tail__'] = e.tail
            for k, g in groupby(e, lambda x: x.tag):
                g = [_xml2d(x) for x in g]
                kids[k] = g
            return kids
        return { parent.tag : _xml2d(parent) }

    @staticmethod
    def _convertDictToXML(parent):
        def _d2xml(d, p):
            for k,v in d.items():
                if isinstance(v,dict):
                    node = etree.SubElement(p,k)
                    _d2xml(v,node)
                elif isinstance(v,list):
                    for item in v:
                        node = etree.SubElement(p, k)
                        _d2xml(item, node)
                elif k == '__content__':
                    p.text = v
                elif k == '__tail__':
                    p.tail = v
                else:
                    p.set(k,v)
        k,v = d.items()[0]
        node = etree.Element(k)
        _d2xml(v,node)
        return node

    # TODO
    @staticmethod
    def _convertDictToKwargs(args):
        def _attrToKwargs(var, attr, out):
            val = var[attr]
            if isinstance(val, dict):
                for arg, d in val.iteritems():
                    # print "GORB" + str(arg) + " " + str(d)
                    _attrToKwargs(var[attr], arg, out)
            else:
                out[attr] = var[attr][0]['__content__']

        out = {}
        for key, val in args.iteritems():
            for attr in val:
                if attr is not '__content__' and attr is not '__tail__':
                    _attrToKwargs(val, attr, out)
                    # print '\tATTR: ' + attr + ' VAL: ' + str(val[attr])
                    # out[attr] = val[attr][0]['__content__']
                    # out[key] = val.get(attr)                   
        return out

    def __init__(self, inxmlfile=''):
        self._filename = inxmlfile
        self._root = None

        if inxmlfile != '':
            self.parseXMLFile(inxmlfile)

    def parseXMLString(self, inxmlstring):
        self._root = ET.fromstring(inxmlstring)

    def parseXMLFile(self, inxmlfile):
        self._root = ET.parse(inxmlfile).getroot()

    def findAll(self, name):
        out = []
        for elem in self._root.iter(name):
            d = MetaData._convertXMLToDict(elem)
            kwargs = MetaData._convertDictToKwargs(d)
            out.append(kwargs)
        return out
