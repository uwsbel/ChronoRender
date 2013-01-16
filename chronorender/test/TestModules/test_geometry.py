import unittest
from chronorender.cr import ChronoRender
from chronorender.geometry import Geometry

class GeometryTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        # self._factory = self._cr._factories.getFactory(Geometry.getTypeName())

    def tearDown(self):
        del self._cr
        # del self._factory

    def test_geoSphere(self):
        return True
        # sph = self._factory.build(Sphere.getTypeName())
        # sph = Sphere()
        # self.assertEqual(sph.getTypeName(), Sphere.getTypeName())
