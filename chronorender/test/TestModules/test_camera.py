import unittest
from camera import Camera
from cr_scriptable import Scriptable
from finder import Finder
from metadata import MetaData

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        finder = Finder(['./input/scripts'])
        meta = MetaData('./input/metadata/yaml/3.yaml')
        data = meta.singleFromType(Camera)
        cam = Camera(**data)
        cam.resolveAssets(finder)
        cam.render(None)                   
