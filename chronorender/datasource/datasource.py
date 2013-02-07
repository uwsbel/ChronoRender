from chronorender.data.ds.base import DataSource
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

    def __init__(self, name="default", resource="", *args, **kwargs):
        super(DataSource,self).__init__(*args, **kwargs)

        self.name = name
        self.resource = self.getMember('resource')

    def _initMembersDict(self):
        self._members['resource'] = [str, '']

    def updateMembers(self):
        self.setMember('resource', self.resource)

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
