import unittest

# load environment so can get chronorender
import sys
import inspect
import os

script_file = inspect.getfile(inspect.currentframe())
script_path = os.path.dirname(os.path.abspath(script_file))
modtest_path = os.path.split(script_path)[0]
mod_path = os.path.split(modtest_path)[0]
sys.path.append(mod_path)

import chronorender as cr

class test_function_foo(unittest.TestCase):
    def test_function_foo(self):
        self.assertTrue(cr.main.foo())

class test_RndrObjects(unittest.TestCase):
    def test_flyweight(self):
        obj1 = cr.RndrObject.RndrObject("obj1")
        obj2 = cr.RndrObject.RndrObject("obj2")
        objCloneOf1 = cr.RndrObject.RndrObject("obj1")

        if id(obj1) == id(obj2):
            return False
        if id(obj1) != id(objCloneOf1):
            return False
        return True

class test_DataProcessor(unittest.TestCase):
    @staticmethod
    def createRenderObjects():
        objs = []
        for i in range(0,10):
            obj_name = "obj" + str(i)
            obj = cr.RndrObject.RndrObject(obj_name)
            objs.append(obj)
        return objs

    def test_function_dumpRIBToFile(self):
        objs = test_DataProcessor.createRenderObjects()
        data_proc = cr.DataProcessor.DataProcessor()
        infile = "./testcases/stationary/0.dat"
        outfile = "output/test_function_dumpRIBToFile.out"

        data_proc.dumpRIBToFile(objs, infile, outfile)

        if os.path.exists(outfile) != True:
            return False

        return True

    def test_function_dumpRIBToStdOut(self):
        objs = test_DataProcessor.createRenderObjects()
        data_proc = cr.DataProcessor.DataProcessor()
        infile = "./testcases/stationary/0.dat"

        data_proc.dumpRIBToStdOut(objs, infile)

        return True

    def test_function_dumpRIBToStdOut_Large(self):
        objs = test_DataProcessor.createRenderObjects()
        data_proc = cr.DataProcessor.DataProcessor()
        infile = "./testcases/large/0.dat"

        data_proc.dumpRIBToStdOut(objs, infile)

        return True

class test_MetaData(unittest.TestCase):
    def test_function_parse(self):
        md = cr.MetaData.MetaData()
        xmlfile = 'testcases/xml/0.xml'

        f = open(xmlfile, 'r')
        xml = f.read()
        md.parseXML(xml)

        settings = md.findAll('settings')
        for inst in settings:
            s = cr.RndrSettings.RndrSettings(**inst)
            print s

        return True

if __name__ == '__main__':
    unittest.main()
