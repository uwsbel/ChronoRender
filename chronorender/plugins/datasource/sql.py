# -*- coding: utf-8 -*-

import data.ds.base
import data.metadata
from datasource import DataSource

try:
    import sqlalchemy

    # (sql type, storage type, analytical type)
    _sql_to_brewery_types = (
        (sqlalchemy.types.UnicodeText, "text", "typeless"),
        (sqlalchemy.types.Text, "text", "typeless"),
        (sqlalchemy.types.Unicode, "string", "set"),
        (sqlalchemy.types.String, "string", "set"),
        (sqlalchemy.types.Integer, "integer", "discrete"),
        (sqlalchemy.types.Numeric, "float", "range"),
        (sqlalchemy.types.DateTime, "date", "typeless"),
        (sqlalchemy.types.Date, "date", "typeless"),
        (sqlalchemy.types.Time, "unknown", "typeless"),
        (sqlalchemy.types.Interval, "unknown", "typeless"),
        (sqlalchemy.types.Boolean, "boolean", "flag"),
        (sqlalchemy.types.Binary, "unknown", "typeless")
    )

    concrete_sql_type_map = {
        "string": sqlalchemy.types.Unicode,
        "text": sqlalchemy.types.UnicodeText,
        "date": sqlalchemy.types.Date,
        "time": sqlalchemy.types.DateTime,
        "integer": sqlalchemy.types.Integer,
        "float": sqlalchemy.types.Numeric,
        "boolean": sqlalchemy.types.SmallInteger
    }
except:
    from data.utils import MissingPackage
    sqlalchemy = MissingPackage("sqlalchemy", "SQL streams", "http://www.sqlalchemy.org/",
                                comment = "Recommended version is > 0.7")
    _sql_to_brewery_types = ()
    concrete_sql_type_map = {}

def split_table_schema(table_name):
    """Get schema and table name from table reference.

    Returns: Tuple in form (schema, table)
    """

    split = table_name.split('.')
    if len(split) > 1:
        return (split[0], split[1])
    else:
        return (None, split[0])


class SQLContext(object):
    """Holds context of SQL store operations."""

    def __init__(self, url=None, connection=None, schema=None):
        """Creates a SQL context"""

        if not url and not connection:
            raise AttributeError("Either url or connection should be provided" \
                                 " for SQL data source")

        super(SQLContext, self).__init__()

        if connection:
            self.connection = connection
            self.should_close = False
        else:
            engine = sqlalchemy.create_engine(url)
            self.connection = engine.connect()
            self.should_close = True

        self.metadata = sqlalchemy.MetaData()
        self.metadata.bind = self.connection.engine
        self.schema = schema

    def close(self):
        if self.should_close and self.connection:
            self.connection.close()

    def table(self, name, autoload=True):
        """Get table by name"""

        return sqlalchemy.Table(name, self.metadata,
                                autoload=autoload, schema=self.schema)

def fields_from_table(table):
    """Get fields from a table. Field types are normalized to the Brewery
    data types. Analytical type is set according to a default conversion
    dictionary."""

    fields = []

    for column in table.columns:
        field = data.metadata.Field(name=column.name)
        field.concrete_storage_type = column.type

        for conv in _sql_to_brewery_types:
            if issubclass(column.type.__class__, conv[0]):
                field.storage_type = conv[1]
                field.analytical_type = conv[2]
                break

        if not field.storage_type:
            field.storaget_tpye = "unknown"

        if not field.analytical_type:
            field.analytical_type = "unknown"

        fields.append(field)

    return data.metadata.FieldList(fields)

def concrete_storage_type(field, type_map={}):
    """Derives a concrete storage type for the field based on field conversion
       dictionary"""

    concrete_type = field.concrete_storage_type

    if not isinstance(concrete_type, sqlalchemy.types.TypeEngine):
        if type_map:
            concrete_type = type_map.get(field.storage_type)

        if not concrete_type:
            concrete_type = concrete_sql_type_map.get(field.storage_type)

        if not concrete_type:
            raise ValueError("unable to find concrete storage type for field '%s' "
                             "of type '%s'" % (field.name, field.storage_type))

    return concrete_type

class SQLDataSource(DataSource):
    """docstring for ClassName
    """
    def __init__(self, connection=None, url=None,
                    table=None, statement=None, schema=None, autoinit = True,
                    **options):
        """Creates a relational database data source stream.

        :Attributes:
            * url: SQLAlchemy URL - either this or connection should be specified
            * connection: SQLAlchemy database connection - either this or url should be specified
            * table: table name
            * statement: SQL statement to be used as a data source (not supported yet)
            * autoinit: initialize on creation, no explicit initialize() is
              needed
            * options: SQL alchemy connect() options
        """

        super(SQLDataSource, self).__init__()

        if not table and not statement:
            raise AttributeError("Either table or statement should be " \
                                 "provided for SQL data source")

        if statement:
            raise NotImplementedError("SQL source stream based on statement " \
                                      "is not yet implemented")

        if not options:
            options = {}

        self.url = url
        self.connection = connection

        self.table_name = table
        self.statement = statement
        self.schema = schema
        self.options = options

        self.context = None
        self.table = None
        self.fields = None

        if autoinit:
            self.initialize()

    def initialize(self):
        """Initialize source stream. If the fields are not initialized, then
        they are read from the table.
        """
        if not self.context:
            self.context = SQLContext(self.url, self.connection, self.schema)
        if self.table is None:
            self.table = self.context.table(self.table_name)
        if not self.fields:
            self.read_fields()
        self.field_names = self.fields.names()

    def finalize(self):
        self.context.close()

    def read_fields(self):
        self.fields = fields_from_table(self.table)
        return self.fields

    def rows(self):
        if not self.context:
            raise RuntimeError("Stream is not initialized")
        return self.table.select().execute()

    def records(self):
        if not self.context:
            raise RuntimeError("Stream is not initialized")
        fields = self.field_names
        for row in self.rows():
            record = dict(zip(fields, row))
            yield record

def build(**kwargs):
    return DataSource(**kwargs)
