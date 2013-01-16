import unittest
from chronorender.cr import ChronoRender

class DataProcessorTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()

    def tearDown(self):
        del self._cr
