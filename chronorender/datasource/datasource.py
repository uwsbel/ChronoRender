from data.ds.base import DataSource
import cr_object
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

    def __init__(self, name="default", *args, **kwargs):
        super(DataSource,self).__init__(*args, **kwargs)

        self.name = name

    def _initMembersDict(self):
        return

    def getInputDataFiles(self):
        return
        # return glob.glob(self.settings._in)

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
