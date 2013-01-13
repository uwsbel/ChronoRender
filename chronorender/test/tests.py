# load environment so can get chronorender
import sys, inspect, os

def setPythonPathForCRImport():
    script_file = inspect.getfile(inspect.currentframe())
    script_path = os.path.dirname(os.path.abspath(script_file))
    modtest_path = os.path.split(script_path)[0]
    mod_path = os.path.split(modtest_path)[0]
    sys.path.append(mod_path)

setPythonPathForCRImport()

import unittest
import TestModules as tm
import chronorender as cr

class test_function_foo(unittest.TestCase):
    def test_function_foo(self):
        self.assertTrue(cr.main.foo())

# class test_RndrObjects(unittest.TestCase):

def getTestSuites(modules):
    suite1 = tm.test_data_processor.TestSuite()
    suite2 = tm.test_meta_data.TestSuite()
    suite3 = tm.test_ri_stream.TestSuite()
    suite4 = tm.test_rndr_settings.TestSuite()
    suite5 = tm.test_cri_stream.TestSuite()
    suite6 = tm.test_shader.TestSuite()
    return [suite1, suite2, suite3, suite4, suite5, suite6]


def setCWDToTestDir():
    testpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
    os.chdir(os.path.dirname(testpath))

if __name__ == '__main__':
    setCWDToTestDir()   # do this for the sake of relative paths used in tests

    modules = []
    alltests = unittest.TestSuite(getTestSuites(modules))
    for suite in alltests:
        unittest.TextTestRunner(verbosity=2).run(suite)

    # unittest.main()      
