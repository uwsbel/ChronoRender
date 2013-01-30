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
        target = 'output/gorb.rib'
        aqsis = self.fact.build('aqsis')
        aqsis.init()
        aqsis.startRenderContext(target)
        aqsis.FrameBegin(0)
        aqsis.FrameEnd()
        aqsis.stopRenderContext()
        aqsis.cleanup()

        self._verifyAndRemoveTarget(target)

    def test_prman(self):
        # only test if on system
        if not which('render'):
            return

        target = 'output/prman.rib'
        # target = '-'
        prman = self.fact.build('prman')
        prman.init()
        prman.startRenderContext(target)
        prman.Attribute("searchpath", {"shader" : "./"})
        prman.FrameBegin(666)
        prman.WorldBegin()
        for i in range(0, 1):
          prman.Sphere(1 ,-1, 1, 360)
        prman.WorldEnd()
        prman.FrameEnd()
        prman.stopRenderContext()
        prman.cleanup()

        self._verifyAndRemoveTarget(target)

    def test_prman_directrender(self):
        # only test if on system
        if not which('render'):
            return

        target = 'output/prman.tif'
        prman = self.fact.build('prman')
        prman.init()
        prman.startRenderContext()
        prman.FrameBegin(666)
        prman.Display(target, 'tiff', 'rgba')
        prman.WorldBegin()
        for i in range(0, 10):
          prman.TransformBegin()
          prman.Translate(0, i*0.1, i*0.5)
          prman.Sphere(0.1 ,-0.1, 0.1, 360)
          prman.TransformEnd()
        prman.WorldEnd()
        prman.FrameEnd()
        prman.stopRenderContext()
        prman.cleanup()

        self._verifyAndRemoveTarget(target)
        

    def _verifyAndRemoveTarget(self, target):
        self.assertTrue(os.path.exists(target))
        os.remove(target)
