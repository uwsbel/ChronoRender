import unittest
from camera import Camera
from cr_scriptable import Scriptable
from finder import Finder
from metadata import MetaData

class ScriptableTestCase(unittest.TestCase):
    def test_create(self):
        finder = Finder(['./input/scripts'])
        meta = MetaData('./input/metadata/yaml/3.yaml')
        data = meta.singleFromType(Camera)
        cam = Camera(**data)
        cam.resolveAssets(finder)
        cam.render(None)                   

    def test_script(self):
        finder = Finder(['./input/scripts'])
        scry = Scriptable(file="camera_script.py", function="render")
        cam = Camera()
        cam.script = scry
        cam.resolveAssets(finder)
        cam.render(None)                   
