import unittest, os

import chronorender as cr

class FinderTestCase(unittest.TestCase):
    def test_resolvePathToAbsolute(self):
        input_paths = ['./', './input']
        finder = cr.Finder(input_paths)
        comp_paths = []
        for path in input_paths:
            comp_paths.append(os.path.abspath(path))

        paths = finder.getSearchPaths()
        for i in range(0, len(input_paths)):
            self.assertEquals(comp_paths[i], paths[i])

    def test_addPathsList(self):
        input_paths = ['./', './input']
        finder = cr.Finder([])
        comp_paths = []
        for path in input_paths:
            comp_paths.append(os.path.abspath(path))

        finder.addPathsList(input_paths)

        paths = finder.getSearchPaths()
        for i in range(0, len(input_paths)):
            self.assertEquals(comp_paths[i], paths[i])

    def test_givenFullPath(self):
        inpath = './input/shaders/plastic.sl'
        finder = cr.Finder([inpath])

        out = finder.find('plastic.sl')

        self.assertEquals(out, os.path.abspath(inpath))
