import unittest
from chronorender.cr import ChronoRender

import chronorender.datasource as ds
import chronorender.metadata as md

class DataSourceTestCase(unittest.TestCase):
    def setUp(self):
        self._factories = ChronoRender().getFactories(ds.DataSource.getTypeName())

    def tearDown(self):
        del self._factories

    def test_csvDataSource(self):
        import csv
        meta = md.MetaData('./input/metadata/yaml/1.yaml')
        infile = './input/data/stationary/0.dat'
        csvsrc = self._factories.build('csv', resource=infile,
                fields=[["gorb", "integer"], "test", "test2", "n4", "n5", "n6", "n7"])

        csvsrc.initialize()
        rows = []
        reader = csvsrc.rows()
        for row in reader:
            rows.append(row)

        csvrows = []
        with open(infile, 'rb') as csvfile:
            read = csv.reader(csvfile)
            for row in read:
                csvrows.append(row)

        self.assertTrue(len(csvrows), len(rows))
        for i in range(0, len(rows)):
            for j in range(0, len(rows[i])):
                self.assertEqual(str(csvrows[i][j]), str(rows[i][j]))
