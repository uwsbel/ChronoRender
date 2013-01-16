import unittest
from chronorender.cr import ChronoRender
from lighting import Lighting

class LightingTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories.getFactory(Lighting.getTypeName())

    def tearDown(self):
        del self._cr
        del self._factory

    def test_lightingFactory(self):
        create = self._factory.build(Lighting.getTypeName())
        self.assertTrue(create != None)
