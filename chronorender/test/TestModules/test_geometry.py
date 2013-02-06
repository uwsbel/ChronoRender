import unittest, os, shutil
from chronorender import ChronoRender
from chronorender.geometry import Geometry, Sphere
# from chronorender.geometry import File

class GeometryTestCase(unittest.TestCase):
    def test_geoSphere(self):
        sph = Sphere()
        self.assertEqual(sph.getTypeName(), Sphere.getTypeName())

    # def test_geoFile(self):
        # expected_dir = './output'
        # out_arc = os.path.join(expected_dir, 'ARCHIVES')
        # out_sdr = os.path.join(expected_dir, 'SHADERS')
        # out_tex = os.path.join(expected_dir, 'TEXTURES')
        # expected_out = os.path.join(out_arc, 'goom.rib')

        # geo = File()
        # geo.filename = 'goom.obj'
        # geo.filepath = os.path.abspath('./input/files/goom.obj')
        # geo._generateRIBArchive(geo.filepath, geo._getNewFilename(),
                # out_arc, out_sdr, out_tex)

        # self.assertTrue(os.path.exists(expected_dir))
        # self.assertTrue(os.path.exists(expected_out))

        # shutil.rmtree(out_arc)
