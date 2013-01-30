import unittest, os

from chronorender.renderer import RendererFactory
from chronorender.cr_utils import which

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

    def test_prman(self):
        # only test if on system
        if not which('render'):
            return

        prman = self.fact.build('prman')
        prman.init()
        prman.startRenderContext('output/prman.rib')
        prman.FrameBegin(666)
        prman.WorldBegin()
        for i in range(0, 10):
          prman.Sphere(1 ,-1, 1, 360)
        prman.WorldEnd()
        prman.FrameEnd()
        prman.stopRenderContext()
        prman.cleanup()
