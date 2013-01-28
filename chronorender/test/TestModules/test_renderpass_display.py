import unittest, os

import chronorender.renderpass.display as rpass

class RenderPassDisplayTestCase(unittest.TestCase):

    def test_evalOutName(self):
        postfix = "000"
        outpath = "OUTPUT"
        disp = rpass.Display()

        name = disp._evalOutName(outpath, postfix)

        expected = os.path.join("OUTPUT", "default.000")
        self.assertEqual(name, expected)

    def test_evalOutName2(self):
        postfix = "000"
        outpath = "OUTPUT"
        disp = rpass.Display()
        disp.output = "out.tif"

        name = disp._evalOutName(outpath, postfix)
        expected = os.path.join("OUTPUT", "out.000.tif")

        self.assertEqual(name, expected)
