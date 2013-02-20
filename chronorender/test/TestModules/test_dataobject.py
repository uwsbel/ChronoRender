import unittest
from chronorender import ChronoRender
from chronorender.finder import FinderFactory

import chronorender.data as dat
import chronorender.datasource as ds
import chronorender.metadata as md

class DataObjectTestCase(unittest.TestCase):
    def setUp(self):
        self._factories = ChronoRender().getFactories(dat.DataObject.getTypeName())

    def tearDown(self):
        del self._factories

    def test_build(self):
        meta = md.MetaData('./input/metadata/yaml/1.yaml')
        ddata = meta.listFromType(dat.DataObject)
        self.assertTrue(len(ddata) > 0)

        for data in ddata:
            dobj = self._factories.build(dat.DataObject.getTypeName(), **data)
            self.assertTrue(len(dobj._datasrcs) > 0)
            self.assertTrue(len(dobj._dataprocs) > 0)

    def test_multipleResources(self):
        cr = ChronoRender()
        meta = md.MetaData('./input/metadata/yaml/1.yaml')
        args = meta.singleFromType(dat.DataObject)
        dataobj = dat.DataObject(cr._factories, **args)
        dataobj._resolveSources()

        poses = []
        for i in range(0, 3):
            for row in dataobj.getData(i):
                poses.append(row['pos_x'])
        self.assertTrue(0.0 in poses)
        self.assertTrue(1.0 in poses)
        self.assertTrue(2.0 in poses)

    def test_datasrcScript(self):
        cr = ChronoRender()
        meta = md.MetaData('./input/metadata/yaml/datasrc_script.yml')
        args = meta.singleFromType(dat.DataObject)
        dataobj = dat.DataObject(cr._factories, **args)
        finder = FinderFactory.build(['./input'])
        dataobj.resolveAssets(finder)

        poses = []
        for i in range(0, 3):
            for row in dataobj.getData(i):
                poses.append(row['pos_x'])
        self.assertTrue(0.0 in poses)
        self.assertTrue(1.0 in poses)
        self.assertTrue(2.0 in poses)
