'''Test cr_for_maya, need maya and pymel installed and in the PYTHONPATH in
order to work'''
import sys, inspect, os

def setPythonPathForImport():
    script_file = inspect.getfile(inspect.currentframe())
    script_path = os.path.dirname(os.path.abspath(script_file))
    modtest_path = os.path.split(script_path)[0]
    mod_path = os.path.split(modtest_path)[0]
    main_path = os.path.join(modtest_path , 'test')
    main_path = os.path.join(main_path, 'TestModules')

    # ChronoRender path
    cr_path = os.path.dirname(mod_path)

    # cr_for_maya path
    crm_path = os.path.join(modtest_path, 'RMS')
    crm_path = os.path.join(crm_path, 'RMS_python')

    sys.path.append(main_path)
    sys.path.append(mod_path)
    sys.path.append(cr_path)
    sys.path.append(crm_path)


setPythonPathForImport()
import unittest, argparse, glob

def getTestSuites(modfilter, expr=''):
    inmodules = glob.glob(expr)

    if len(inmodules) <= 0:
        return

    module_strings = [os.path.splitext(os.path.split(str)[1])[0] for str in inmodules]

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
    parser.add_argument('-s', help="suppress test output",
            action="store_true")

    args = parser.parse_args()

    _stdout = sys.stdout
    if args.s:
        null = open(os.devnull, 'wb')
        sys.stdout = null

    alltests = getTestSuites(args.modules, 'TestModules/test_*.py')

    for suite in alltests:
        unittest.TextTestRunner(verbosity=2).run(suite)

    sys.stdout = _stdout
