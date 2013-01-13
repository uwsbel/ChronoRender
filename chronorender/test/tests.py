# load environment so can get chronorender
import sys, inspect, os, glob, argparse

def setPythonPathForCRImport():
    script_file = inspect.getfile(inspect.currentframe())
    script_path = os.path.dirname(os.path.abspath(script_file))
    modtest_path = os.path.split(script_path)[0]
    mod_path = os.path.split(modtest_path)[0]
    modtest_path += '/test/TestModules'
    sys.path.append(modtest_path)
    sys.path.append(mod_path)


setPythonPathForCRImport()
import unittest
import chronorender as cr


def getTestSuites(modfilter):
    inmodules = glob.glob('TestModules/test_*.py')
    module_strings = [''+str[12:len(str)-3] for str in inmodules]
    impmods = module_strings
    if len(modfilter) != 0:
        impmods = [mod for mod in module_strings if mod in modfilter]
    modules = map(__import__, impmods)
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

def setCWDToTestDir():
    testpath = os.path.abspath(inspect.getfile(inspect.currentframe()))
    os.chdir(os.path.dirname(testpath))

if __name__ == '__main__':
    setCWDToTestDir()   # do this for the sake of relative paths used in tests

    parser = argparse.ArgumentParser(description='run tests')
    parser.add_argument('modules', metavar='N', type=str, nargs='*', help='list of test modules to run')

    args = parser.parse_args()
    alltests = getTestSuites(args.modules)
    for suite in alltests:
        unittest.TextTestRunner(verbosity=2).run(suite)

    # unittest.main()      
