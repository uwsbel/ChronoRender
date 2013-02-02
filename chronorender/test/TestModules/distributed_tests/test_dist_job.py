import unittest, os, glob
import chronorender as cr
import chronorender.rndr_job as rndr
import chronorender.prog as prog

class RndrJobTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = cr.ChronoRender()
        self.infile = './input/metadata/yaml/job/dist2.yml'

    def tearDown(self):
        del self._cr
        del self.infile

    def test_submitJob(self):
        currdir = os.getcwd()
        job = rndr.RndrJob(self.infile, self._cr._factories)
        job.stream = 'prman'
        p = prog.CRenderLocal()
        try:
            job.submit(p)
            files = glob.glob('./input/metadata/yaml/job/OUTPUT/*.sh')
            for f in files:
                os.remove(f)
        finally:
            os.chdir(currdir)
