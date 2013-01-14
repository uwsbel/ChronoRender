import unittest
from chronorender.cr import ChronoRender

class ChronoRenderTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()

    def tearDown(self):
        del self._cr

    def test_createRenderJob(self):
        inxml = './input/xml/0.xml'

        self._cr.createRenderJob(inxml)
