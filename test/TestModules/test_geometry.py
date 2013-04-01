import unittest, os, shutil
from chronorender import ChronoRender
from chronorender.renderer import Stdout
from chronorender.geometry import Geometry, Sphere, Archive

import chronorender.plugins as pm
from chronorender.renderer import RendererFactory
# from chronorender.geometry import File

class GeometryTestCase(unittest.TestCase):
    @staticmethod
    def _createGeoFactories():
        cr = ChronoRender()
        factories = cr.getFactories()
        fact = factories.getFactory('geometry')
        return fact

    @staticmethod
    def _createRenderer():
        renderer_fact = RendererFactory()
        rib = renderer_fact.build('stdout')
        rib.init()
        return rib

    def test_geoSphere(self):
        sph = Sphere()
        self.assertEqual(sph.getTypeName(), Sphere.getTypeName())

    def test_Archive(self):
        arch = Archive(filename='default_scene.rib')
        return True


    def test_Plugins(self):
        geo_fact = GeometryTestCase._createGeoFactories()
        rib = GeometryTestCase._createRenderer()

        geo = geo_fact.build('cube')
        geo .addParameter('string test', 'asdgsd')
        print geo
        geo.render(rib);
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

