import unittest, os

from chronorender.renderer import RendererFactory

class RendererTestCase(unittest.TestCase):
    def setUp(self):
        self.fact = RendererFactory()

    def tearDown(self):
        del self.fact

    def test_create(self):
        prman = self.fact.build('prman')
        self.assertTrue(prman)

    def test_context(self):
        aqsis = self.fact.build('aqsis')
        aqsis.init()
        aqsis.startRenderContext('output/gorb.rib')
        aqsis.FrameBegin(0)
        aqsis.FrameEnd()
        aqsis.stopRenderContext()
        aqsis.cleanup()
