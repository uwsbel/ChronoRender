import unittest

import chronorender.converter as conv

class ImporterTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_OBJImport(self):
        objimp = conv.OBJConverter()
        objimp.convert('./input/files/goom.obj', './output/goob.rib')
