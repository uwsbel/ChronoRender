import unittest, os, shutil
from chronorender.cr import ChronoRender
from chronorender.geometry import Geometry, Sphere, File
from chronorender.finder import FinderFactory
# from chronorender.ri import RiStream

class GeometryTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories.getFactory(Geometry.getTypeName())

    def tearDown(self):
        del self._cr
        del self._factory

    def test_geoSphere(self):
        sph = self._factory.build(Sphere.getTypeName())
        sph = Sphere()
        self.assertEqual(sph.getTypeName(), Sphere.getTypeName())

    def test_geoFile(self):
        expected_dir = './output/ARCHIVES'
        expected_out = os.path.join(expected_dir, 'goom.rib')
        geo = File()
        geo.filename = './input/files/goom.obj'
        finder = FinderFactory.build(['./input'])

        geo.resolveAssets(finder, './output')

        # rib = RiStream('str')
        # geo.render(rib)
        # print rib.getText()

        self.assertTrue(os.path.exists(expected_dir))
        self.assertTrue(os.path.exists(expected_out))

        shutil.rmtree(expected_dir)
