import unittest, os

from chronorender.finder import FinderFactory

class FinderTestCase(unittest.TestCase):
    def test_resolvePathToAbsolute(self):
        input_paths = ['./', './input']
        finder = FinderFactory.build(input_paths)
        comp_paths = []
        for path in input_paths:
            comp_paths.append(os.path.abspath(path))

        paths = finder.getSearchPaths()
        for i in range(0, len(input_paths)):
            self.assertEquals(comp_paths[i], paths[i])

    def test_findDIR(self):
        finder = FinderFactory.build(['./'])
        path = None
        comp_path = os.path.abspath('input')
        path = finder.find('test/input')
        self.assertEqual(comp_path, path)

    def test_findFile(self):
        finder = FinderFactory.build(['./'])
        path = None
        comp_path = os.path.abspath('input/data/stationary/0.dat')
        path = finder.find('test/input/data/stationary/0.dat')
        self.assertEqual(comp_path, path)
