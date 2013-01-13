import unittest
from chronorender.plugin_manager import PluginManager

class PluginManagerTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_initFromConfig(self):
        man = PluginManager()
        self.assertTrue('factory' in man._plugins)
        self.assertTrue('geometry' in man._plugins['factory'])

    def test_loadPlugins(self):
        man = PluginManager()
        man.loadPlugins()
        self.assertTrue('sphere' in man._plugins['factory']['geometry']['plugins'])

    def test_registerPlugins(self):
        man = PluginManager()
        man.loadPlugins()
        self.assertTrue(man.registerPlugins(), True)

    def test_getPlugins(self):
        man = PluginManager()

        man.loadPlugins()
        man.registerPlugins()
        geomods = man.getPlugins('factory','geometry')

        self.assertTrue(len(geomods) > 0)
