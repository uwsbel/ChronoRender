import unittest
from chronorender.data import DataObject
from chronorender.datasource import CSVDataSource, DataSource
from chronorender.simulation import Simulation
from chronorender.renderobject import RenderObject
from chronorender.geometry import Sphere

from chronorender.metadata import MDReaderFactory

class SimulationTestCase(unittest.TestCase):
    def test_simulation(self):
        datasrc = CSVDataSource(resource='input/data/stationary/*.dat', delim=',', fields= [["id", "integer"], ["pos_z", "float"], ["pos_y", "float"], ["pos_x", "float"], ["euler_x", "float"], ["euler_y", "float"], ["euler_z", "float"]])
        dataobj = DataObject()
        dataobj.addDataSource(datasrc)

        sph = Sphere()
        robj = RenderObject(condition="id > 0", geometry=[sph.getSerialized()])

        sim = Simulation()
        sim.setData(dataobj)
        sim.addRenderObject(robj)

        md = MDReaderFactory.build('sim.yml')
        md.addElement(Simulation.getTypeName(), sim.getSerialized())
        md.writeToDisk()
