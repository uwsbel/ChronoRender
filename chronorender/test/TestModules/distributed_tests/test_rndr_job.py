import unittest
import chronorender as cr
import chronorender.rndr_job as rndr
import os

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        self.infile = './input/metadata/yaml/job/3.yaml'

    def tearDown(self):
        del self._cr
        del self.infile

    def test_submitJob(self):
        currdir = os.getcwd()
        job = rndr.RndrJob(self.infile, self._cr._factories)
        try:
            job.submit()
        finally:
            os.chdir(currdir)
