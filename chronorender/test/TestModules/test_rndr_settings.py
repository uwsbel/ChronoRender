import unittest

from chronorender.rendersettings import RenderSettings
from chronorender.metadata import MetaData

import sys, os

class RenderSettingsTestCase(unittest.TestCase):
    def setUp(self):
        infile = './input/metadata/yaml/0.yaml'
        self.md = MetaData(infile)

        settings = self.md.findAll('rendersettings')
        if len(settings) <= 0:
            raise Exception('invalid settings')

        self.settings = RenderSettings(**settings[0])

    def tearDown(self):
        del self.md
        del self.settings

    def test_SearchPaths(self):
        print self.settings.searchpaths
