import unittest
import chronorender as cr
import chronorender.shader as shader

from chronorender.metadata import MetaData

import sys, os, pprint

class MetaDataTestCase(unittest.TestCase):
    def test_XML(self):
        infile_xml = './input/metadata/xml/0.xml'
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
            sdr = shader.Shader(**inst)
            self.assertEqual(sdr.getMember('Kd'), '666')

        elems = md.getElementsDict()
        # pprint.pprint(elems)

    def test_YAML(self):
        infile_yaml = './input/metadata/yaml/0.yaml'
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
        self.assertEqual(len(shdr), 1)

        # elems = md.getElementsDict()
        # pprint.pprint(elems)

    def test_AddElem(self):
        md = MetaData('out.yml')
        md.addElement('test', {'gorb' : 'val'})

        elems = md.getElementsDict()
        self.assertTrue('test' in elems)

    def test_Write(self):
        infile_yaml = './input/metadata/yaml/3.yaml'
        md = MetaData(infile_yaml)

        md.addElement('test', {'gorb' : 'val'})

        md.writeToDisk('out.yml')

        self.assertTrue(os.path.exists('out.yml'))
        os.remove('out.yml')


def TestSuite():
    tests = ['test_function_parse']
    return unittest.TestSuite(map(MetaDataTestCase, tests))
