import unittest
from chronorender.ri import RiStream

class RiStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.ri = RiStream('str')

    def tearDown(self):
        del self.ri

    def test_write(self):
        self.ri.RiFrameBegin(1)
        self.ri.write('test\n')
        self.ri.RiFrameEnd()
