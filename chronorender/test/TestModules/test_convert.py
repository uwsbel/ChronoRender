import unittest, os, shutil

import chronorender.converter as conv

class ImporterTestCase(unittest.TestCase):
    def setUp(self):
        return

    def tearDown(self):
        return

    def test_OBJConvert(self):
        expected_dir = './output'
        out_arc = os.path.join(expected_dir, 'ARCHIVES')
        out_sdr = os.path.join(expected_dir, 'SHADERS')
        out_tex = os.path.join(expected_dir, 'TEXTURES')
        expected_out = os.path.join(out_arc, 'goob.rib')
        src = os.path.abspath('./input/files/goom.obj')

        objimp = conv.ConverterFactory.build(src)
        objimp.convert('./output/goob.rib',
                archive_outpath = out_arc,
                shader_outpath = out_sdr,
                texture_outpath = out_tex)

        self.assertTrue(os.path.exists(out_arc))
        self.assertTrue(os.path.exists(expected_out))

        shutil.rmtree(out_arc)
        if os.path.exists(out_sdr):
            shutil.rmtree(out_sdr)
        if os.path.exists(out_tex):
            shutil.rmtree(out_tex)
