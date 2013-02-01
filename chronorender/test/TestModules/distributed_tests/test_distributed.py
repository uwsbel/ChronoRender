import unittest, os

from chronorender.distributed import Distributed, DistributedFactory
import chronorender as cr
import chronorender.rndr_job as rndr
import chronorender.prog as prog

class DistributedTestCase(unittest.TestCase):

    def setUp(self):
        self.cr = cr.ChronoRender()
        # fact = DistributedFactory()
        self.fact = self.cr._factories.getFactory(Distributed.getTypeName())

        try:
          self.dist = self.fact.build('pbs')
        except Exception:
          self._delAssets()

    def tearDown(self):
        self._delAssets()

    def test_factory(self):
        self.assertTrue(self.dist != None)

    def test_connection(self):

        self.dist.initialize()
        cid = self.dist.getConnection()
        self.dist.end()

        self.assertTrue(cid != None)

    def test_submit(self):
        self.dist.initialize()
        job = self.dist.createJobTemplate()
        self.dist.submit(job)
        self.dist.end()

    def _delAssets(self):
        del self.cr
        del self.dist
