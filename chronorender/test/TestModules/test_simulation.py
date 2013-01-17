import unittest
import chronorender.cr as cr
from cr_object import Object
import chronorender.simulation as sim
import chronorender.metadata as md
import chronorender.data as dat

class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        meta = md.MetaData('./input/metadata/yaml/simulation.yaml')
        data = meta.singleFromType(sim.Simulation)
        self._sim = sim.Simulation(factories=self._cr._factories, **data)

    def tearDown(self):
        del self._cr
        del self._sim

    def test_simulationFactory(self):
        self.assertTrue(True != False)
