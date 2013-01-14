import unittest
from chronorender.cr import ChronoRender
from simulation import Simulation

class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories[Simulation.getTypeName()]

    def tearDown(self):
        del self._cr

    def test_simulationFactory(self):
        create = self._factory.build(Simulation.getTypeName())
        self.assertTrue(create != None)
