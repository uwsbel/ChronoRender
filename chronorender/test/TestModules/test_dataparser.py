import unittest
from chronorender.cr import ChronoRender

class DataParserTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()

    def tearDown(self):
        del self._cr

    def test_createAndRunRenderJob(self):
        inxml = './input/xml/0.xml'
