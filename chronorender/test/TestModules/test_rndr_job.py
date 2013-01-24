import unittest
import chronorender as cr
import os

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()

    def tearDown(self):
        del self._cr

    def test_initJob(self):
        infile = './input/metadata/yaml/job/3.yaml'
        job = cr.RndrJob(infile, self._cr._factories)

    # def test_runJob(self):
        # currdir = os.getcwd()
        # job = cr.RndrJob(self.infile, self._cr._factories)
        # try:
            # job.run()                           
        # finally:
            # os.chdir(currdir)

    # def test_instantiateOnDisk(self):
        # currdir = os.getcwd()
        # job = cr.RndrJob(self.infile, self._cr._factories)
        # try:
            # job.createOutDirs()
            # job.makeAssetsRelative()
        # finally:
            # os.chdir(currdir)

    def test_runCriJob(self):
        infile = './input/metadata/yaml/job/cornell.yaml'
        currdir = os.getcwd()
        job = cr.RndrJob(infile, self._cr._factories)
        try:
            job.run('aqsis')                           
        finally:
            os.chdir(currdir)

