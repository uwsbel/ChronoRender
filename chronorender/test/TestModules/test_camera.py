import unittest
from camera import Camera
from finder import FinderFactory
from metadata import MetaData
from chronorender.ri import RiStream

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        filen = "default_camera.rib"
        cam = Camera(filename=filen)
        self.assertEqual(cam.filename, filen)
