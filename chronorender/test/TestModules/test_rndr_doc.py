import unittest, os
import chronorender as cr

from metadata import MetaData

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        md = MetaData('./input/metadata/yaml/3.yaml')
        self.doc = cr.RndrDoc(self._cr._factories, md)

    def tearDown(self):
        del self.doc

    def test_initFromMetadata(self):
        return

    # TODO
    def test_resolveAssets(self):
        self.doc.resolveAssets()

    def test_render(self):
        ri = cr.RiStream('str')
        self.doc.render(ri, 0)
