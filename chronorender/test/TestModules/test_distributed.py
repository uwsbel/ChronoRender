import unittest, os

from chronorender.distributed import Distributed, DistributedFactory

class DistributedTestCase(unittest.TestCase):

    def setUp(self):
        fact = DistributedFactory()
        self.dist = fact.build()

    def tearDown(self):
        del self.dist

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
        print 'QUEUE', job.queue
        self.dist.submit(job)
        self.dist.end()
        return
