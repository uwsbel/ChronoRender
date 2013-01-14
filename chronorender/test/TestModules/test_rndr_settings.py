import unittest
import chronorender as cr

import sys, os

class RenderSettingsTestCase(unittest.TestCase):
    def setUp(self):
        self.md = cr.MetaData()
        self.md.parseXMLFile('input/xml/0.xml')

        settings = self.md.findAll('rendersettings')
        if len(settings) <= 0:
            raise Exception('invalid settings')

        self.settings = cr.RenderSettings(**settings[0])

    def tearDown(self):
        del self.md
        del self.settings
