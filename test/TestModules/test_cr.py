import unittest
from chronorender import ChronoRender

class ChronoRenderTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()

    def tearDown(self):
        del self._cr

    def test_create(self):
        self.assertTrue(True)
    # def test_createAndRunRenderJob(self):
        # inxml = './input/metadata/xml/0.xml'

        # self._cr.createAndRunRenderJob(inxml)

    def test_FactoryClasses(self):
        factories = self._cr.getFactories()
        fact = factories.getFactory('datasource')

        for cls in fact.getClasses():
            print cls, cls.getTypeName()
