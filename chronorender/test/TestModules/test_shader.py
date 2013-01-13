import unittest
import chronorender as cr

class ShaderTestCase(unittest.TestCase):
    def setUp(self):
        self.sdr = cr.Shader(name='./input/shaders/plastic.sl')

    def tearDown(self):
        del self.sdr

    def test_parameters(self):
        newKa = 666.0
        newColor = [0.6, 0.6, 0.6]
        params = self.sdr.getParameters()

        # check params
        self.assertTrue('Ka' in params)
        self.assertEqual(type(params['Ka']), float)
        self.assertTrue('specularcolor' in params)
        self.assertEqual(type(params['specularcolor']), list)

        # set params
        params['Ka'] = newKa
        params['specularcolor'] = newColor

        # verify params
        check = self.sdr.getParameters()
        self.assertEqual(newKa, check['Ka'])
        self.assertEqual(newColor, check['specularcolor'])

def TestSuite():
    tests = ['test_parameters']
    return unittest.TestSuite(map(ShaderTestCase, tests))
