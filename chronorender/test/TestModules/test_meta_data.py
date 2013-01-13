import unittest
import chronorender as cr

import sys, os

class MetaDataTestCase(unittest.TestCase):
    def setUp(self):
        self.md = cr.MetaData()
        self.infile_xml = './input/xml/0.xml'

    def tearDown(self):
        del self.md

    # TODO
    def test_function_parse(self):
        self.md.parseXMLFile(self.infile_xml)

        elem = self.md.findAll('settings')
        for inst in elem:
            s = cr.RndrSettings(**inst)
        elem = self.md.findAll('renderobject')
        for inst in elem:
            robj = cr.RndrObject(**inst)
        elem = self.md.findAll('renderpass')
        for inst in elem:
            rpass = cr.RndrPass(**inst)
        elem = self.md.findAll('geometry')
        for inst in elem:
            geo = cr.Geometry(**inst)
        elem = self.md.findAll('shader')
        for inst in elem:
            sdr = cr.Shader(**inst)
            self.assertEqual(sdr.getInfo().name, 'plastic')
            self.assertEqual(sdr.getInfo().type, 'surface')
            self.assertEqual(sdr.getParameters()['Kd'], 666.0)

def TestSuite():
    tests = ['test_function_parse']
    return unittest.TestSuite(map(MetaDataTestCase, tests))
