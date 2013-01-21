import unittest
from chronorender.cr import ChronoRender
from lighting import Lighting
from finder import FinderFactory
from metadata import MetaData
from chronorender.ri import RiStream

class LightingTestCase(unittest.TestCase):
    def test_create(self):
        finder = FinderFactory.build(['./input/shaders'])
        meta = MetaData('./input/metadata/yaml/3.yaml')
        data = meta.singleFromType(Lighting)
        light = Lighting(**data)
        light.resolveAssets(finder)
        ri = RiStream('str')
        light.render(ri)                   
        print ri.getText()
