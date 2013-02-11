import unittest, os

from chronorender.camera import Camera
from chronorender.renderobject import RenderObject
from chronorender.cr_scriptable import Scriptable
from chronorender.geometry import Sphere

class ScriptableTestCase(unittest.TestCase):
    def test_script(self):
        scriptfile = os.path.abspath('./input/scripts/camera_script.py')
        scry = Scriptable()
        scry.scriptpath = scriptfile
        scry.function = 'render'
        scry._parseModInformation()

        # cam = Camera()
        cam = RenderObject()
        cam.script = scry
        cam.geometry = [Sphere()]
        cam.render(None)                   
