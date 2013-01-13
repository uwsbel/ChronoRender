import unittest
import chronorender as cr

class RndrDocTestCase(unittest.TestCase):
    def setUp(self):
        self.doc = cr.RndrDoc()

    def tearDown(self):
        del self.doc

    def test_resolveAssetPaths(self):
        self.assertEqual('this','that')
        return

def TestSuite():
    tests = ['test_render']
    return unittest.TestSuite(map(RndrDocTestCase, tests))
