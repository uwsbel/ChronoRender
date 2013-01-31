from movie import Movie
from ffmpeg import FFMPEG
import chronorender.plugins.plugin_manager as pm
import chronorender.factory as fact

class MovieFactoryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class MovieFactory():
    def build(self, movie, **kwargs):
        if movie == FFMPEG.getTypeName():
            return FFMPEG(**kwargs)
        elif self._factory:
            return self._factory.build(movie, **kwargs)
        else:
            raise MovieFactoryException('movie encoder: \"' + movie + '\" is not supported')

    def __init__(self):
        self._plugins = None
        self._factory = None

        self._loadPlugins()
        self._loadFactory()

    def _loadPlugins(self):
        plugs = pm.PluginManager()
        plugs.loadPluginsFor(fact.Factory.getTypeName(), Movie.getTypeName())
        plugs.registerPluginsFor(fact.Factory.getTypeName(), Movie.getTypeName())
        self._plugins = plugs.getPlugins(fact.Factory.getTypeName(), Movie.getTypeName())

    def _loadFactory(self):
        if len(self._plugins) <= 0:
            return

        self._factory = fact.Factory(Movie.getTypeName())
        for plug in self._plugins:
            self._factory.addModule(plug)
