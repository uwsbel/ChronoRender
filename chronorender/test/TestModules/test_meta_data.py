import unittest
import chronorender as cr

from metadata import MetaData

import sys, os

class MetaDataTestCase(unittest.TestCase):
    def test_XML(self):
        infile_xml = './input/xml/0.xml'
        md = MetaData(infile_xml)

        elem = md.findAll('rendersettings')
        self.assertEqual(len(elem), 1)

        elem = md.findAll('renderobject')
        self.assertEqual(len(elem), 1)

        elem = md.findAll('renderpass')
        self.assertEqual(len(elem), 1)

        elem = md.findAll('geometry')
        self.assertEqual(len(elem), 1)

        elem = md.findAll('shader')
        self.assertEqual(len(elem), 1)
        for inst in elem:
            sdr = cr.Shader(**inst)
            self.assertEqual(sdr.getMember('Kd'), '666')

    def test_YANML(self):
        infile_yaml = './input/yaml/0.yaml'
        md = MetaData(infile_yaml)

        sett = md.findAll('rendersettings')
        self.assertEqual(len(sett), 1)

        robj = md.findAll('renderobject')
        self.assertEqual(len(robj), 1)

        rpass = md.findAll('renderpass')
        self.assertEqual(len(rpass), 1)

        geom = md.findAll('geometry')
        self.assertEqual(len(geom), 1)

        shdr = md.findAll('shader')
        self.assertEqual(len(shdr), 2)

def TestSuite():
    tests = ['test_function_parse']
    return unittest.TestSuite(map(MetaDataTestCase, tests))
