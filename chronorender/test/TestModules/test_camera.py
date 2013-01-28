import unittest
from camera import Camera

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        filen = "default_camera.rib"
        cam = Camera(filename=filen)
        self.assertEqual(cam.filename, filen)
