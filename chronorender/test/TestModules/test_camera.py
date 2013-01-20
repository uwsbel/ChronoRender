import unittest
from camera import Camera
from finder import Finder
from metadata import MetaData
from ri_stream import RiStream

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        finder = Finder(['./input/scripts'])
        meta = MetaData('./input/metadata/yaml/3.yaml')
        data = meta.singleFromType(Camera)
        cam = Camera(**data)
        cam.resolveAssets(finder)
        ri = RiStream('str')
        cam.render(ri)                   
        print ri.getText()
