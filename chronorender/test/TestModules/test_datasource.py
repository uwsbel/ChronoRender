import unittest
from chronorender.cr import ChronoRender

from chronorender.datasource import DataSource

class DataSourceTestCase(unittest.TestCase):
    def setUp(self):
        self._factories = ChronoRender().getFactories(DataSource.getTypeName())

    def tearDown(self):
        del self._factories

    # def test_csvDataSource(self):
        # md = MetaData('./input/yaml/1.yaml')
        # self._data = CSVDataSource()
