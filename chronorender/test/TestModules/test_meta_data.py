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
            s = cr.RenderSettings(**inst)
        elem = self.md.findAll('renderobject')
        for inst in elem:
            robj = cr.RenderObject(**inst)
        elem = self.md.findAll('renderpass')
        for inst in elem:
            rpass = cr.RenderPass(**inst)
        elem = self.md.findAll('geometry')
        for inst in elem:
            geo = cr.Geometry(**inst)
        elem = self.md.findAll('shader')
        for inst in elem:
            sdr = cr.Shader(**inst)
            self.assertEqual(sdr.getMember('Kd'), '666')

def TestSuite():
    tests = ['test_function_parse']
    return unittest.TestSuite(map(MetaDataTestCase, tests))