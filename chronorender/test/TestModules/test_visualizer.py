import unittest
from chronorender.cr import ChronoRender
from visualizer import Visualizer

class VisualizerTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()

    def tearDown(self):
        del self._cr

    def test_createAndRunRenderJob(self):
        create = self._factory.build(Simulation.getTypeName())
        self.assertTrue(create != None)
