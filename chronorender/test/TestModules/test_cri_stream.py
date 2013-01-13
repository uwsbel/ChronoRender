import unittest
import chronorender as cr

class CRiStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.ri = cr.cri_stream.loadRI("ri")

    def tearDown(self):
        del self.ri

    def test_render(self):
        self.ri.RiBegin(self.ri.RI_NULL)
        self.ri.RiFrameBegin(1)
        self.ri.RiWorldBegin()
        self.ri.RiSurface("plastic")
        self.ri.RiTranslate(3,0,0)
        self.ri.RiSphere(1,-1,1,360)
        self.ri.RiWorldEnd()
        self.ri.RiFrameEnd()
        self.ri.RiEnd()

def TestSuite():
    tests = ['test_render']
    return unittest.TestSuite(map(CRiStreamTestCase, tests))
