import unittest
import chronorender as cr

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self.doc = cr.RndrDoc()

    def tearDown(self):
        del self.doc

    def test_initFromMetadata(self):
        md = cr.MetaData()
        infile_xml = './input/xml/0.xml'
        md.parseXMLFile(infile_xml)

        self.doc.initFromMetadata(md)
        print self.doc.geometry

    # TODO
    def test_resolveAssets(self):
        self.doc.resolveAssets()

def TestSuite():
    tests = ['test_render']
    return unittest.TestSuite(map(RndrDocTestCase, tests))
