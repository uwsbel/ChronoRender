from chronorender.data.ds.base import Field
from chronorender.data.dq import FieldTypeProbe
import time
from chronorender.data.metadata import expand_record
from chronorender.datasource import DataSource

try:
    from pyes.es import ES
except ImportError:
    from chronorender.data.utils import MissingPackage
    pyes = MissingPackage("pyes", "ElasticSearch streams", "http://www.elasticsearch.org/")

class ESDataSource(DataSource):
    @staticmethod
    def getTypeName():
        return "elasticsearch"
    """docstring for ClassName
    """
    def __init__(self, document_type='', database=None, host=None, port=None,
                 expand=False, **elasticsearch_args):
        super(ESDataSource, self).__init__(**elasticsearch_args)
        """Creates a ElasticSearch data source stream.

        :Attributes:
            * document_type: elasticsearch document_type name
            * database: database name
            * host: elasticsearch database server host, default is ``localhost``
            * port: elasticsearch port, default is ``27017``
            * expand: expand dictionary values and treat children as top-level keys with dot '.'
                separated key path to the child..
        """
        self.document_type = self.getVar('document_type', elasticsearch_args)
        self.database_name = self.getVar('database', elasticsearch_args)
        self.host = self.getVar('host', elasticsearch_args)
        self.port = self.getVar('port', elasticsearch_args)
        self.elasticsearch_args = elasticsearch_args
        self.expand = expand
        self.connection = None
        self._fields = None

    def _initMembersDict(self):
        super(ESDataSource, self)._initMembersDict()
        self._members['document_type'] = [str, ""]
        self._members['database'] = [str, ""]
        self._members['host'] = [str, None]
        self._members['port'] = [str, None]

    def updateMembers(self):
        super(ESDataSource, self).updateMembers()
        self.setMember('document_type', self.document_type)
        self.setMember('database_name', self.database_name)
        self.setMember('port', self.port)
        self.setMember('host', self.host)

    def initialize(self):
        """Initialize ElasticSearch source stream:
        """
        args = self.elasticsearch_args.copy()
        server = ""
        if self.host:
            server = self.host
        if self.port:
            server += ":" + self.port

        self.connection = ES(server, **args)
        self.connection.default_indices = self.database_name
        self.connection.default_types = self.document_type

    def read_fields(self, limit=0):
        keys = []
        probes = {}

        def probe_record(record, parent=None):
            for key, value in record.items():
                if parent:
                    full_key = parent + "." + key
                else:
                    full_key = key

                if self.expand and type(value) == dict:
                    probe_record(value, full_key)
                    continue

                if not full_key in probes:
                    probe = FieldTypeProbe(full_key)
                    probes[full_key] = probe
                    keys.append(full_key)
                else:
                    probe = probes[full_key]
                probe.probe(value)

        for record in self.document_type.find(limit=limit):
            probe_record(record)

        fields = []

        for key in keys:
            probe = probes[key]
            field = Field(probe.field)

            storage_type = probe.unique_storage_type
            if not storage_type:
                field.storage_type = "unknown"
            elif storage_type == "unicode":
                field.storage_type = "string"
            else:
                field.storage_type = "unknown"
                field.concrete_storage_type = storage_type

            # FIXME: Set analytical type

            fields.append(field)

        self.fields = list(fields)
        return self.fields

    def rows(self):
        if not self.connection:
            raise RuntimeError("Stream is not initialized")
        from pyes.query import MatchAllQuery
        fields = self.fields.names()
        results = self.connection.search(MatchAllQuery(), search_type="scan", timeout="5m", size="200")
        return ESRowIterator(results, fields)

    def records(self):
        if not self.connection:
            raise RuntimeError("Stream is not initialized")
        from pyes.query import MatchAllQuery
        results = self.connection.search(MatchAllQuery(), search_type="scan", timeout="5m", size="200")
        return ESRecordIterator(results, self.expand)

class ESRowIterator(object):
    """Wrapper for ElasticSearch ResultSet to be able to return rows() as tuples and records() as
    dictionaries"""
    def __init__(self, resultset, field_names):
        self.resultset = resultset
        self.field_names = field_names

    def __getitem__(self, index):
        record = self.resultset.__getitem__(index)

        array = []

        for field in self.field_names:
            value = record
            for key in field.split('.'):
                if key in value:
                    value = value[key]
                else:
                    break
            array.append(value)

        return tuple(array)

class ESRecordIterator(object):
    """Wrapper for ElasticSearch ResultSet to be able to return rows() as tuples and records() as
    dictionaries"""
    def __init__(self, resultset, expand=False):
        self.resultset = resultset
        self.expand = expand

    def __getitem__(self, index):
        def expand_record(record, parent=None):
            ret = {}
            for key, value in record.items():
                if parent:
                    full_key = parent + "." + key
                else:
                    full_key = key

                if type(value) == dict:
                    expanded = expand_record(value, full_key)
                    ret.update(expanded)
                else:
                    ret[full_key] = value
            return ret

        record = self.resultset.__getitem__(index)
        if not self.expand:
            return record
        else:
            return expand_record(record)

def build(**kwargs):
    return ESDataSource(**kwargs)
