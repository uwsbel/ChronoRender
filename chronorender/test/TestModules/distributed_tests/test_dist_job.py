import unittest, os
import chronorender as cr
import chronorender.rndr_job as rndr
import chronorender.prog as prog

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        self.infile = './input/metadata/yaml/job/dist.yml'

    def tearDown(self):
        del self._cr
        del self.infile

    def test_submitJob(self):
        currdir = os.getcwd()
        job = rndr.RndrJob(self.infile, self._cr._factories)
        p = prog.CRenderLocal()
        print p, p.args, p.getProgCall()
        try:
            job.submit(p)
        finally:
            os.chdir(currdir)
