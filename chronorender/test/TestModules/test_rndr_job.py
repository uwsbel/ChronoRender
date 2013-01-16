import unittest
import chronorender as cr

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        self._infilexml = './input/metadata/xml/0.xml'

    def tearDown(self):
        del self._cr
        del self._infilexml

    def test_initJob(self):
        job = cr.RndrJob(self._infilexml, self._cr._factories)

    def test_runJob(self):
        job = cr.RndrJob(self._infilexml, self._cr._factories)
        job.run()
