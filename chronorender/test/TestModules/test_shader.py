import unittest, os.path
import chronorender as cr

from chronorender.finder import FinderFactory
from chronorender.ri import RiStream

class ShaderTestCase(unittest.TestCase):
    def setUp(self):
        self.sdr = cr.Shader(name='plastic.sl')
        self.sdr._shdrpath = os.path.abspath('./input/shaders/plastic.sl')
        self.sdr._initShaderParameters()

    def tearDown(self):
        del self.sdr

    def test_constructWithFullPath(self):
        self.sdr = cr.Shader(shdrpath='./input/shaders/plastic.sl')
        self.assertEqual(self.sdr.getShaderType(), 'surface')

    def test_setAsset(self):
        param = 'Kd'
        vtype = type(self.sdr._paramdict[param])

        self.sdr.setAsset(param, 555)

        self.assertEqual(555, self.sdr._paramdict[param])
        self.assertEqual(type(self.sdr._paramdict[param]), vtype)

    def test_parameters(self):
        newKa = 666.0
        newColor = [0.6, 0.6, 0.6]
        params = self.sdr._paramdict

        # check params
        self.assertTrue('Ka' in params)
        self.assertEqual(type(params['Ka']), float)
        self.assertTrue('specularcolor' in params)
        self.assertEqual(type(params['specularcolor']), list)

        # set params
        params['Ka'] = newKa
        params['specularcolor'] = newColor

        # verify params
        check = self.sdr._paramdict
        self.assertEqual(newKa, check['Ka'])
        self.assertEqual(newColor, check['specularcolor'])

    def test_render(self):
        ri = RiStream('str')
        self.sdr.render(ri)
        print ri.getText()
