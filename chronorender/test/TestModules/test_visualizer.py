import unittest
from chronorender.cr import ChronoRender
from visualizer import Visualizer

class VisualizerTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories[Visualizer.getTypeName()]

    def tearDown(self):
        del self._cr

    def test_createAndRunRenderJob(self):
        create = self._factory.build(Visualizer.getTypeName())
        self.assertTrue(create != None)
