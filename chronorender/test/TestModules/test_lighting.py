import unittest
from lighting import Lighting

class LightingTestCase(unittest.TestCase):
    def test_create(self):
        lgtfile = 'default_lighting.rib'
        light = Lighting()
        light.filename = lgtfile

        self.assertEqual(light.filename, lgtfile)
