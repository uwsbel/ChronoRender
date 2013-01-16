import unittest
from chronorender.cr import ChronoRender
from scene import Scene

class SceneTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories.getFactory(Scene.getTypeName())

    def tearDown(self):
        del self._cr
        del self._factory

    def test_sceneFactory(self):
        create = self._factory.build(Scene.getTypeName())
        self.assertTrue(create != None)
