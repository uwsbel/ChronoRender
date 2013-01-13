import xml.etree.ElementTree as ET

class MetaDataException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MetaData():
    @staticmethod
    def _convertXMLToDict(parent):
        ret = {}
        if parent.items(): ret.update(dict(parent.items()))
        if parent.text: ret['__content__'] = parent.text
        if ('List' in parent.tag):
            ret['__list__'] = []
            for elem in parent:
                ret['__list__'].append(MetaData._convertXMLToDict(elem))
        else:
            for elem in parent:
                ret[elem.tag] = MetaData._convertXMLToDict(elem)
        return ret

    @staticmethod
    def _convertDictToKwargs(args):
        out = {}
        for key, val in args.iteritems():
            if type(val) == dict:
                out[key] = val.get('__content__')
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
            out.append(MetaData._convertDictToKwargs(d))
        return out
