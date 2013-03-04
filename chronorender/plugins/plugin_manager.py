import chronorender.thirdparty.yaml as yaml
import inspect, os, glob, sys
from pkg_resources import resource_string, resource_filename, resource_stream

class PluginManagerException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PluginManager():
    _defaultConfigFile = 'plugin_manager.yml'

    @staticmethod
    def _getModuleName(path):
        return os.path.splitext(os.path.split(path)[1])[0]

    def __init__(self):
        self._configpath = './'
        self._plugins = {}
        self._initPlugins(self._findDefaultConfigFile())

    def _initPlugins(self, inyaml):
        # f = open(inyaml)
        f = resource_stream(__name__, PluginManager._defaultConfigFile)
        data = yaml.safe_load(f)
        f.close()
        self._plugins.update(data)

    def _findDefaultConfigFile(self):
        self._configpath = os.path.dirname(resource_filename(__name__,
            PluginManager._defaultConfigFile))
        return os.path.join(self._configpath, PluginManager._defaultConfigFile)

    def _getPaths(self, pathstr):
        curr_path = os.getcwd()
        try:
            os.chdir(self._configpath)
            out = []
            paths = pathstr.split(':')
            for path in paths:
                if os.path.exists(path):
                    out.append(os.path.abspath(path)+os.sep)
        except:
            pass
        finally:
            os.chdir(curr_path)
        return out

    # find all the src files for plugins
    def loadPlugins(self):
        for plugintype, val in self._plugins.iteritems():
            for pluginname in val.iterkeys():
                self.loadPluginsFor(plugintype, pluginname)

    def loadPluginsFor(self, plugintype, typename):
        conc_plugin = self.getPluginType(plugintype, typename)

        # for pluginname, vals in plugins.iteritems():
        if 'paths' not in conc_plugin: 
            self._plugins[plugintype][typename]['paths'] = []
        if 'plugins' not in conc_plugin:
            self._plugins[plugintype][typename]['plugins'] = []

        conc_plugin['paths'] = self._getPaths(conc_plugin['paths'])
        for path in conc_plugin['paths']:
            conc_plugin['plugins'] = [PluginManager._getModuleName(x) for x in glob.glob(path+'*.py*')]
            

    def registerPlugins(self):
        for plugintype, val in self._plugins.iteritems():
            for pluginname in val.iterkeys():
                self.registerPluginsFor(plugintype, pluginname)

    def registerPluginsFor(self, plugintype, typename):
        conc_plugin = self.getPluginType(plugintype, typename)

        paths = conc_plugin['paths']
        for path in paths:
            if path not in sys.path:
                sys.path.insert(0,path)
        conc_plugin['modules'] = []
        for plugin in conc_plugin['plugins']:
            try:
                conc_plugin['modules'].append(__import__(plugin))
            except Exception as e:
              # print "unable to load plugin: ", plugin, plugintype, typename
              # print "\t", e 
              pass
            finally:
              pass

    def getPlugins(self, plugintype, pluginname):
        if plugintype not in self._plugins:
            return []
        elif pluginname not in self._plugins[plugintype]:
            return []
        else:
            return self._plugins[plugintype][pluginname]['modules']

    def getPluginType(self, plugintype, pluginname):
        if plugintype not in self._plugins:
            raise PluginManagerException('no plugin type: ' + plugintype)
        elif pluginname not in self._plugins[plugintype]:
            raise PluginManagerException('no plugin name: ' + pluginname + ' for plugin type: ' + plugintype)
        return self._plugins[plugintype][pluginname]

    def removePlugin(self, plugintype, pluginname):
        del self._plugins[plugintype][pluginname]
