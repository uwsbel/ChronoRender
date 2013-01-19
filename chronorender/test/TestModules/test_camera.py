import unittest
from camera import Camera

class CameraTestCase(unittest.TestCase):
    def test_create(self):
        cam = Camera(filename="gorb.rib")

        print cam
