import unittest
import chronorender.cr as cr
from cr_object import Object
import chronorender.simulation as sim
import chronorender.metadata as md
import chronorender.data as dat
import chronorender.renderobject as cro
from chronorender.finder import FinderFactory

class SimulationTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        meta = md.MetaData('./input/metadata/yaml/simulation.yaml')
        data = meta.singleFromType(sim.Simulation)
        self._sim = sim.Simulation(factories=self._cr._factories, **data)
        finder = FinderFactory.build(['./input'])
        self._sim.resolveAssets(finder)

    def tearDown(self):
        del self._cr
        del self._sim

    def test_simulationFactory(self):
        for robj in self._sim._robjs:
            print "CONDITION: " + robj.condition
            for row in self._sim._data.getData(0, robj.condition):
                print row
        self.assertTrue(True != False)
