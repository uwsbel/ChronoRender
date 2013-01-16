import unittest
import chronorender as cr

from metadata import MetaData

import sys, os

class RIBGenertorTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        md = MetaData('./input/metadata/yaml/1.yaml')
        self.data_proc = cr.RIBGenerator(self._cr._factories, md)
        self.objs = []
        for i in range(0,10):
            self.objs.append(cr.RenderObject("obj"+str(i)))
        self.infile_stationary = './input/data/stationary/0.dat'

    def tearDown(self):
        del self.data_proc
        del self.objs

    def test_function_dumpRIBToFile(self):
        outfile = "output/test_function_dumpRIBToFile.out"

        self.data_proc.dumpRIBToFile(self.objs, self.infile_stationary, outfile)

        self.assertTrue(os.path.exists(outfile))

    # TODO
    def test_function_dumpRIBToStdOut(self):
        self.data_proc.dumpRIBToStdOut(self.objs, self.infile_stationary)

        return True

    # TODO
    def test_function_dumpRIBToStdOut_Large(self):
        self.data_proc.dumpRIBToStdOut(self.objs, self.infile_stationary)

        return True
