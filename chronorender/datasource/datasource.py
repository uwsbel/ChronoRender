from chronorender.data.ds.base import DataSource
from chronorender.cr_scriptable import Scriptable
import chronorender.cr_object as cr_object
import glob, os
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

class DataSource(DataSource, cr_object.Object):
    @staticmethod
    def getInstanceQualifier():
        return "type"

    @staticmethod
    def getTypeName():
        return "datasource"

    def getBaseName(self):
        return DataSource.getTypeName()

    def __init__(self, name="default", resource="", *args, **kwargs):
        super(DataSource,self).__init__(*args, **kwargs)

        self.name = self.getMember('name')
        self.resource = self.getMember('resource')
        self.script     = self.getMember(Scriptable.getTypeName())

    def _initMembersDict(self):
        super(DataSource, self)._initMembersDict()

        self._members['name']     = [str, '']
        self._members['resource'] = [str, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]

    def updateMembers(self):
        super(DataSource, self).updateMembers()

        self.setMember('name', self.name)
        self.setMember('resource', self.resource)
        self.setMember(Scriptable.getTypeName(), self.script)

    def resolveAssets(self, assetman):
        out = []
        # if self.script:
            # out.extend(self.script.resolveAssets(assetman))
        return out

    def getInputResources(self):
        path = os.path.abspath(self.resource)
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
