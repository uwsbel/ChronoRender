import unittest
from chronorender.cr import ChronoRender
from chronorender.scene import Scene

from chronorender.renderpass.settings import Settings

class SceneTestCase(unittest.TestCase):
    def setUp(self):
        self._cr = ChronoRender()
        self._factory = self._cr._factories.getFactory(Scene.getTypeName())

    def tearDown(self):
        del self._cr
        del self._factory

    def test_create(self):
        s = Scene(filename="gorb.rib")
        print "filanem: " + s.filename

        sett = Settings(resolution=[122,122])
        print sett.resolution

    def test_sceneFactory(self):
        create = self._factory.build(Scene.getTypeName())
        self.assertTrue(create != None)
