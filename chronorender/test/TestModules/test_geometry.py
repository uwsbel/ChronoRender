import unittest
from chronorender.cr import ChronoRender
from geometry import Geometry
from sphere import Sphere

class GeometryTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories[Geometry.getTypeName()]

    def tearDown(self):
        del self._cr
        del self._factory

    def test_geoFactory(self):
        sph = self._factory.build(Sphere.getTypeName())

        self.assertEqual(sph.getTypeName(), Sphere.getTypeName())
