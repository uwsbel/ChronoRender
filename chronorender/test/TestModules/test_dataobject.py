import unittest
from chronorender.cr import ChronoRender

import chronorender.data as ds
import chronorender.metadata as md

class DataObjectTestCase(unittest.TestCase):
    def setUp(self):
        self._factories = ChronoRender().getFactories(ds.DataObject.getTypeName())

    def tearDown(self):
        del self._factories

    def test_build(self):
        meta = md.MetaData('./input/metadata/yaml/1.yaml')
        ddata = meta.listFromType(ds.DataObject)
        self.assertTrue(len(ddata) > 0)

        for data in ddata:
            dobj = self._factories.build(ds.DataObject.getTypeName(), **data)
            self.assertTrue(len(dobj._datasrcs) > 0)
            self.assertTrue(len(dobj._dataprocs) > 0)

    def test_run(self):
        return True
