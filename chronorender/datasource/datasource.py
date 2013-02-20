from chronorender.data.ds.base import DataSource
from chronorender.cr_scriptable import Scriptable
from chronorender.cr_object import Object
import chronorender.cr_types as cr_types
import glob, os
import pdb
# Should implement:
# * fields
# * prepare()
# * rows() - returns iterable with value tuples
# * records() - returns iterable with dictionaries of key-value pairs

class DataSourceException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DataSource(Object, DataSource):
    @staticmethod
    def getInstanceQualifier():
        return "type"

    @staticmethod
    def getTypeName():
        return "datasource"

    def getBaseName(self):
        return DataSource.getTypeName()

    def __init__(self, *args, **kwargs):
        super(DataSource,self).__init__(*args, **kwargs)

        self.name = self.getVar('name', kwargs)
        self.resource = self.getVar('resource', kwargs)
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(DataSource, self)._initMembersDict()

        self._members['name']     = [str, 'default']
        self._members['resource'] = [cr_types.url, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def updateMembers(self):
        super(DataSource, self).updateMembers()

        self.setMember('name', self.name)
        self.setMember('resource', self.resource)
        self.setMember(Scriptable.getTypeName(), self.script)

    def resolveAssets(self, assetman):
        out = []
        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        self.resource = assetman.find(self.resource)
        return out

    def getInputResources(self):
        path = self.resource
        if not os.path.isabs(path):
            path = os.path.join(os.getcwd(), self.resource)
        return glob.glob(path)

    def initialize(self):
        return
        
    def finalize(self):
        return 

    def rows(self):
        return

    def records(self):
        return

def build(**kwargs):
    return DataSource(**kwargs)
