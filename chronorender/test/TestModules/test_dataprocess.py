import unittest

from chronorender import ChronoRender
import chronorender.data as dat
import chronorender.datatarget as dt
import chronorender.dataprocess as dp
import chronorender.datasource as ds

class DataProcessTestCase(unittest.TestCase):
    def setUp(self):
        cr = ChronoRender()
        self._factories = cr.getFactories(dp.DataProcess.getTypeName())
        self._srcfactories = cr.getFactories(ds.DataSource.getTypeName())

    def tearDown(self):
        del self._factories

    def test_PassThrough(self):
        infile = './input/data/stationary/0.dat'
        output = dt.DataTarget()
        src = ds.DataSourceNode(self._srcfactories.build('csv', resource=infile, fields=[["gorb", "integer"], "test", "test2", "n4", "n5", "n6", "n7"]))

        nodes = {
                    "source": src,
                    "passthrough": self._factories.build(dp.DataProcess().getTypeName()),
                    "out": output
                }

        connections = [ ("source", "passthrough"), ("passthrough", "out") ]
        stream = dat.Stream(nodes, connections)

        stream.run()
        

        src.initialize()
        counter = 0
        odata = output.data
        for record in src.records:
            self.assertEqual(record, odata[counter])
            counter += 1
        src.finalize()

    def test_Select(self):
        infile = './input/data/ascending/0.dat'
        output = dt.DataTarget()
        src = ds.DataSourceNode(self._srcfactories.build('csv', resource=infile, fields=[["id", "integer"], "test", "test2", "n4", "n5", "n6", "n7"]))

        nodes = {
                    "source": src,
                    "select": self._factories.build(dp.SelectNode.getTypeName(), condition="id >= 5"),
                    "out": output
                }

        connections = [ ("source", "select"), ("select", "out") ]
        stream = dat.Stream(nodes, connections)

        stream.run()
        

        odata = output.data
        counter = 0
        for row in odata:
            counter += 1
        self.assertEqual(counter, 5)

    def test_Derive(self):
        infile = './input/data/ascending/0.dat'
        output = dt.DataTarget()
        src = ds.DataSourceNode(self._srcfactories.build('csv', resource=infile, fields=[["id", "integer"], "test", "test2", "n4", "n5", "n6", "n7"]))

        nodes = {
                    "source": src,
                    "gorb": self._factories.build('derive', formula="id*10", field_name="gorb"),
                    "out": output
                }

        connections =   [ 
                        ("source", "gorb"), 
                        ("gorb", "out") 
                        ]
        stream = dat.Stream(nodes, connections)

        stream.run()
        
        src.initialize()
        counter = 0
        odata = output.data
        for row in src.records:
            self.assertEqual(row['id']*10, odata[counter]['gorb'])
            counter += 1
        src.finalize()

    def test_MultipleProcs(self):
        infile = './input/data/ascending/0.dat'
        output = dt.DataTarget()
        src = ds.DataSourceNode(self._srcfactories.build('csv', resource=infile, fields=[["id", "integer"], "test", "test2", "n4", "n5", "n6", "n7"]))

        nodes = {
                    "source": src,
                    "gorb": self._factories.build('derive', formula="id*10", field_name="gorb"),
                    "select": self._factories.build(dp.SelectNode.getTypeName(), condition="id >= 5"),
                    "out": output
                }

        connections =   [ 
                        ("source", "gorb"), 
                        ("gorb", "select"),
                        ("select", "out") 
                        ]
        stream = dat.Stream(nodes, connections)

        stream.run()
        
        src.initialize()
        counter = 0
        odata = output.data
        for row in src.records:
            if row['id'] >= 5:
                self.assertEqual(row['id']*10, odata[counter]['gorb'])
                counter += 1
        src.finalize()
