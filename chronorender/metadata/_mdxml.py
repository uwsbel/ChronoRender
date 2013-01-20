import xml.etree.ElementTree as ET
from itertools import groupby
from _mdreader import _MDReader
import pprint

class _MDXML(_MDReader):
    @staticmethod
    def getTypeName():
        return "mdreaderxml"

    @staticmethod
    def _convertElemToDict(node):
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
        return { node.tag : _xml2d(node) }

    @staticmethod
    def _convertDictToElem(node):
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
        k,v = node.items()[0]
        elem = etree.Element(k)
        _d2xml(v,elem)
        return elem

    @staticmethod
    def _convertDictToKwargs(args):
        def _attrToKwargs(var, attr, out):
            val = var[attr]
            if isinstance(val, dict):
                for arg, d in val.iteritems():
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

    def __init__(self, inxmlfile):
        self._filename = inxmlfile
        self._root = None

        self._parseFile(inxmlfile)

    def __str__(self):
        return pprint.pformat(self._root)

    def _parseString(self, instring):
        self._root = ET.fromstring(instring)
        return

    def _parseFile(self, infile):
        self._root = ET.parse(infile).getroot()
        return

    def findAll(self, name):
        out = []
        for elem in self._root.iter(name):
            d = _MDXML._convertElemToDict(elem)
            kwargs = _MDXML._convertDictToKwargs(d)
            out.append(kwargs)
        return out

    def getElementsDict(self):
        out = {}
        for elem in self._root:
            d = _MDXML._convertElemToDict(elem)
            kwargs = _MDXML._convertDictToKwargs(d)

            if elem.tag in out:
                out[elem.tag].append(kwargs)
            else:
                out[elem.tag] = [kwargs]
        return out
