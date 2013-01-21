import unittest
from camera import Camera
from finder import FinderFactory
from metadata import MetaData
from chronorender.ri import RiStream

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        finder = FinderFactory.build(['./input/scripts'])
        meta = MetaData('./input/metadata/yaml/3.yaml')
        data = meta.singleFromType(Camera)
        cam = Camera(**data)
        cam.resolveAssets(finder)
        ri = RiStream('str')
        cam.render(ri)                   
        print ri.getText()
