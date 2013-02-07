import unittest
from chronorender import ChronoRender

import chronorender.data as dat
import chronorender.datasource as ds
import chronorender.metadata as md

class SerializeTestCase(unittest.TestCase):
    def setUp(self):
        self.infile = './input/metadata/yaml/3.yaml'

    def test_build(self):
        chron = ChronoRender()
        job = chron.createJob(self.infile)
        for robj in job._rndrdoc.renderables:
            print robj
