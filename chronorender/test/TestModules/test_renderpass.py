import unittest, os

from metadata import MetaData
from renderpass import RenderPass
from chronorender.renderer import RendererFactory

class RenderPassTestCase(unittest.TestCase):
    def setUp(self):
        infile = './input/metadata/yaml/1.yaml'
        md = MetaData(infile)
        self.rpasses = [RenderPass(**x) for x in md.listFromType(RenderPass)]

    def test_create(self):
        for rpass in self.rpasses:
            for settings in rpass.rndrsettings:
                print settings

    def test_render(self):
        fact = RendererFactory()
        ri = fact.build('stdout')
        ri.init()
        for rpass in self.rpasses:
            rpass.render(ri, 0, 0, './')
        ri.cleanup()
