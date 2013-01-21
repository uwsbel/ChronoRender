import unittest, os

import chronorender as cr
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
