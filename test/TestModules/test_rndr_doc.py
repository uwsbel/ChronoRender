import unittest, os

import chronorender as cr
from chronorender.metadata import MetaData
from chronorender.finder import FinderFactory
from chronorender.ri import RiStream

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        md = MetaData('./input/metadata/yaml/3.yaml')
        self.doc = cr.RndrDoc(self._cr._factories, md)

    def tearDown(self):
        del self.doc
