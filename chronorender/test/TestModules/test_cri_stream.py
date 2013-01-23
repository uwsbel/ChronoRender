import unittest
import chronorender.ri as ri

class CRiStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.ri = ri.loadRI("aqsis_core")

    def tearDown(self):
        del self.ri

    def test_render(self):
        radius = 0.5
        self.ri.RiBegin(self.ri.RI_NULL)
        self.ri.RiFrameBegin(1)
        self.ri.RiDisplay("cri.tif", "file", "rgb")
        self.ri.RiWorldBegin()
        self.ri.RiLightSource("pointlight", intensity=0.4)
        self.ri.RiSurface("plastic")
        self.ri.RiColor([0.1, 0.5, 0.5])
        self.ri.RiTranslate(0,0,1)
        self.ri.RiSphere(radius, -radius, radius, 360)
        self.ri.RiWorldEnd()
        self.ri.RiFrameEnd()
        self.ri.RiEnd()
