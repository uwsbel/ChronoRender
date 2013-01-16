#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from .base import SourceNode

class RowListSourceNode(SourceNode):
    """Source node that feeds rows (list/tuple of values) from a list (or any other iterable)
    object."""

    node_info = {
        "label" : "Row List Source",
        "description" : "Provide list of lists or tuples as data source.",
        "protected": True,
        "attributes" : [
            {
                 "name": "list",
                 "description": "List of rows represented as lists or tuples."
            },
            {
                 "name": "fields",
                 "description": "Fields in the list."
            }
        ]
    }
    def __init__(self, a_list = None, fields = None):
        if a_list:
            self.list = a_list
        else:
            self.list = []
        self.fields = fields

    @property
    def output_fields(self):
        if not self.fields:
            raise ValueError("Fields are not initialized")
        return self.fields

    def run(self):
        for row in self.list:
            self.put(row)

class RecordListSourceNode(SourceNode):
    """Source node that feeds records (dictionary objects) from a list (or any other iterable)
    object."""

    node_info = {
        "label" : "Record List Source",
        "description" : "Provide list of dict objects as data source.",
        "protected": True,
        "attributes" : [
            {
                 "name": "a_list",
                 "description": "List of records represented as dictionaries."
            },
            {
                 "name": "fields",
                 "description": "Fields in the list."
            }
        ]
    }

    def __init__(self, a_list=None, fields=None):
        super(RecordListSourceNode, self).__init__()
        if a_list:
            self.list = a_list
        else:
            self.list = []
        self.fields = fields

    @property
    def output_fields(self):
        if not self.fields:
            raise ValueError("Fields are not initialized")
        return self.fields

    def run(self):
        for record in self.list:
            self.put(record)

class StreamSourceNode(SourceNode):
    """Generic data stream source. Wraps a :mod:`brewery.ds` data source and feeds data to the
    output.

    The source data stream should configure fields on initialize().

    Note that this node is only for programatically created processing streams. Not useable
    in visual, web or other stream modelling tools.
    """

    node_info = {
        "label" : "Data Stream Source",
        "icon": "row_list_source_node",
        "description" : "Generic data stream data source node.",
        "protected": True,
        "attributes" : [
            {
                 "name": "stream",
                 "description": "Data stream object."
            }
        ]
    }

    def __init__(self, stream):
        super(StreamSourceNode, self).__init__()
        self.stream = stream

    def initialize(self):
        # if self.stream_type not in data_sources:
        #     raise ValueError("No data source of type '%s'" % stream_type)
        # stream_info = data_sources[self.stream_type]
        # if "class" not in stream_info:
        #     raise ValueError("No stream class specified for data source of type '%s'" % stream_type)

        # self.stream = stream_class(**kwargs)
        # self.stream.fields =
        self.stream.initialize()

    @property
    def output_fields(self):
        return self.stream.fields

    def run(self):
        for row in self.stream.rows():
            self.put(row)

    def finalize(self):
        self.stream.finalize()
