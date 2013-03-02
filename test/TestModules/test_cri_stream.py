import unittest
import chronorender.ri as ri

class CRiStreamTestCase(unittest.TestCase):
    def setUp(self):
        self.ri = ri.loadRI("aqsis_core")

    def tearDown(self):
        del self.ri

    def test_render(self):
        radius = 0.5
        self.ri.Begin(self.ri.RI_NULL)
        self.ri.FrameBegin(1)
        self.ri.Display("cri.tif", "file", "rgb")
        self.ri.WorldBegin()
        self.ri.LightSource("pointlight", intensity=0.4)
        self.ri.Surface("plastic")
        self.ri.Color([0.1, 0.5, 0.5])
        self.ri.Translate(0,0,1)
        self.ri.Sphere(radius, -radius, radius, 360)
        self.ri.WorldEnd()
        self.ri.FrameEnd()
        self.ri.End()
