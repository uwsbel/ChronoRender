import unittest, os
import chronorender as cr

from metadata import MetaData

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        md = MetaData('./input/metadata/xml/0.xml')
        self.doc = cr.RndrDoc(self._cr._factories, md)

    def tearDown(self):
        del self.doc

    def test_initFromMetadata(self):
        return

    # TODO
    def test_resolveAssets(self):
        self.doc._resolveAssets()

    def test_function_getInputDataFiles(self):
        files = self.doc.getInputDataFiles()
        if len(files) != 1:
            return False

        filename = os.path.abspath('./input/data/stationary/0.dat')

        self.assertEqual(files[0], filename)

    def test_function_getOutputFilePath(self):
        outfile = os.path.abspath('./output/xml_0/out_1200.tif')
        retval = self.doc.getOutputDataFilePath(1200)

        self.assertEqual(retval, outfile)
