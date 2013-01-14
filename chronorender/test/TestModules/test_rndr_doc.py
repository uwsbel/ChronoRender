import unittest
import chronorender as cr

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        md = cr.MetaData()
        infile_xml = './input/xml/0.xml'
        md.parseXMLFile(infile_xml)
        self.doc = cr.RndrDoc(md)

    def tearDown(self):
        del self.doc

    def test_initFromMetadata(self):
        print self.doc.geometry

    # TODO
    def test_resolveAssets(self):
        self.doc._resolveAssets()
