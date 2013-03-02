import unittest

from chronorender.factory import Factory
import chronorender.plugins as pm
from chronorender import ChronoRender
from chronorender.datasource import DataSource

class FactoryTestCase(unittest.TestCase):
    def setUp(self):
        self._pm = pm.PluginManager()
        self._pm.loadPlugins()
        self._pm.registerPlugins()

    def tearDown(self):
        del self._pm

    def test_GeoFactory(self):
        fact = Factory('geometry')
        fact.setModules(self._pm.getPlugins('factory','geometry'))

        sph = fact.build('cone')
        self.assertTrue(sph.getTypeName(), 'cone')
        cube = fact.build('cube')
        self.assertTrue(cube.getTypeName(), 'cube')
