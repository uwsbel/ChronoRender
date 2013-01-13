import unittest
import chronorender as cr

import sys, os

class DataProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self.data_proc = cr.DataProcessor()
        self.objs = []
        for i in range(0,10):
            self.objs.append(cr.RndrObject("obj"+str(i)))
        self.infile_stationary = './input/stationary/0.dat'

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

def TestSuite():
    tests = ['test_function_dumpRIBToFile',
                'test_function_dumpRIBToStdOut',
                'test_function_dumpRIBToStdOut_Large']
    return unittest.TestSuite(map(DataProcessorTestCase, tests))
