import unittest, os
import chronorender as cr

from metadata import MetaData
from chronorender.finder import FinderFactory

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        md = MetaData('./input/metadata/yaml/3.yaml')
        self.doc = cr.RndrDoc(self._cr._factories, md)
        self.finder = FinderFactory.build(['./', './input'])

    def tearDown(self):
        del self.doc

    def test_initFromMetadata(self):
        return

    # TODO
    def test_resolveAssets(self):
        self.doc.resolveAssets(self.finder)

    def test_render(self):
        self.doc.resolveAssets(self.finder)
        ri = cr.RiStream('str')
        self.doc.render(ri, 0)
