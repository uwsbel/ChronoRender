import unittest
import chronorender as cr

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        self.infile = './input/metadata/yaml/job/3.yaml'

    def tearDown(self):
        del self._cr
        del self.infile

    def test_initJob(self):
        job = cr.RndrJob(self.infile, self._cr._factories)

    def test_runJob(self):
        job = cr.RndrJob(self.infile, self._cr._factories)
        job.run()                           

    def test_instantiateOnDisk(self):
        job = cr.RndrJob(self.infile, self._cr._factories)
        job.createOutDirs()
        job.makeAssetsRelative()
