import unittest
import chronorender as cr

import sys, os

class RenderSettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.md = cr.MetaData()
        self.md.parseXMLFile('input/xml/0.xml')

        settings = self.md.findAll('rendersettings')
        if len(settings) <= 0:
            raise Exception('invalid settings')

        self.settings = cr.RenderSettings(**settings[0])

    def tearDown(self):
        del self.md
        del self.settings

    def test_function_getInputDataFiles(self):
        files = self.settings.getInputDataFiles()
        if len(files) != 1:
            return False

        filename = os.path.abspath('./input/stationary/0.dat')

        self.assertEqual(files[0], filename)

    def test_function_getOutputFilePath(self):
        outfile = os.path.abspath('./output/out_1200.tif')
        retval = self.settings.getOutputDataFilePath(1200)

        self.assertEqual(retval, outfile)
