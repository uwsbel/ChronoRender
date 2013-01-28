import unittest, os

from camera import Camera
from cr_scriptable import Scriptable

class ScriptableTestCase(unittest.TestCase):
    def test_script(self):
        scriptfile = os.path.abspath('./input/scripts/camera_script.py')
        scry = Scriptable()
        scry.scriptpath = scriptfile
        scry.funcname = 'render'
        scry._parseModInformation()

        cam = Camera()
        cam.script = scry
        cam.render(None)                   
