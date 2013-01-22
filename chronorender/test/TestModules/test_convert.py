import unittest, os, shutil

import chronorender.converter as conv

class ImporterTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_OBJConvert(self):
        src = './input/files/goom.obj'
        expected_dir = './output/ARCHIVES'
        expected_out = os.path.join(expected_dir, 'goob.rib')
        objimp = conv.ConverterFactory.build(src)
        objimp.convert('./output/goob.rib')

        self.assertTrue(os.path.exists(expected_dir))
        self.assertTrue(os.path.exists(expected_out))

        shutil.rmtree(expected_dir)
