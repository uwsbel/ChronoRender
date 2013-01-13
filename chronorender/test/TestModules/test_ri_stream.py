import unittest
import chronorender as cr

class RiStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.ri = cr.RiStream('str')

    def tearDown(self):
        del self.ri

    def test_write(self):
        self.ri.RiFrameBegin(1)
        self.ri.write('test\n')
        self.ri.RiFrameEnd()

def TestSuite():
    tests = ['test_write']
    return unittest.TestSuite(map(RiStreamTestCase, tests))
