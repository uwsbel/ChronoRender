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

# class test_RndrObjects(unittest.TestCase):

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

        self.assertTrue(os.path.exists(outfile))

    # TODO
    def test_function_dumpRIBToStdOut(self):
        objs = test_DataProcessor.createRenderObjects()
        data_proc = cr.DataProcessor.DataProcessor()
        infile = "./testcases/stationary/0.dat"

        data_proc.dumpRIBToStdOut(objs, infile)

        return True

    # TODO
    def test_function_dumpRIBToStdOut_Large(self):
        objs = test_DataProcessor.createRenderObjects()
        data_proc = cr.DataProcessor.DataProcessor()
        infile = "./testcases/large/0.dat"

        data_proc.dumpRIBToStdOut(objs, infile)

        return True

class test_MetaData(unittest.TestCase):
    # TODO
    def test_function_parse(self):
        md = cr.MetaData.MetaData()
        md.parseXMLFile('testcases/xml/0.xml')

        elem = md.findAll('settings')
        for inst in elem:
            s = cr.RndrSettings.RndrSettings(**inst)
        elem = md.findAll('renderobject')
        for inst in elem:
            robj = cr.RndrObject.RndrObject(**inst)
        elem = md.findAll('renderpass')
        for inst in elem:
            rpass = cr.RndrPass.RndrPass(**inst)
        elem = md.findAll('geometry')
        for inst in elem:
            geo = cr.Geometry.Geometry(**inst)
        elem = md.findAll('shader')
        for inst in elem:
            sdr = cr.Shader.Shader(**inst)
        return True

class test_RndrSettings(unittest.TestCase):
    @staticmethod
    def _createAndVerifySettings():
        md = cr.MetaData.MetaData()
        md.parseXMLFile('testcases/xml/0.xml')

        settings = md.findAll('settings')
        if len(settings) <= 0:
            raise Exception('invalid settings')

        return cr.RndrSettings.RndrSettings(**settings[0])

    def test_function_getInputDataFiles(self):
        sett = test_RndrSettings._createAndVerifySettings()
        files = sett.getInputDataFiles()
        if len(files) != 1:
            return False

        filename = os.path.abspath('./testcases/stationary/0.dat')

        self.assertTrue(files[0] == filename)

    def test_function_getOutputFilePath(self):
        sett = test_RndrSettings._createAndVerifySettings()
        outfile = os.path.abspath('./output/out_1200.tif')
        retval = sett.getOutputDataFilePath(1200)

        self.assertTrue(retval == outfile)

if __name__ == '__main__':
    unittest.main()
