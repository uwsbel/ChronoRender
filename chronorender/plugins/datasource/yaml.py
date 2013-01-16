#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import os
import shutil
from datasource import DataSource

try:
    import yaml
except:
    from data.utils import MissingPackage
    yaml = MissingPackage("PyYAML", "YAML directory data source/target", "http://pyyaml.org/")

class YamlDirectoryDataSource(DataSource):
    """docstring for ClassName
    """
    def __init__(self, path, extension="yml", expand=False, filename_field=None):
        """Creates a YAML directory data source stream.
        
        The data source reads files from a directory and treats each file as single record. For example,
        following directory will contain 3 records::
        
            data/
                contract_0.yml
                contract_1.yml
                contract_2.yml
        
        Optionally one can specify a field where file name will be stored.
        
        
        :Attributes:
            * path: directory with YAML files
            * extension: file extension to look for, default is ``yml``,if none is given, then
              all regular files in the directory are read
            * expand: expand dictionary values and treat children as top-level keys with dot '.'
                separated key path to the child.. Default: False
            * filename_field: if present, then filename is streamed in a field with given name,
              or if record is requested, then filename will be in first field.
        
        """
        self.path = path
        self.expand = expand
        self.filename_field = filename_field
        self.extension = extension

    def initialize(self):
        pass

    def records(self):
        files = os.listdir(self.path)

        for base_name in files:
            split = os.path.splitext(base_name)
            if split[1] != self.extension:
                pass

            # Read yaml file
            handle = open(os.path.join(self.path, base_name), "r")
            record = yaml.load(handle)
            handle.close()

            # Include filename in output record if requested
            if self.filename_field:
                record[self.filename_field] = base_name

            yield record

    def rows(self):
        if not self.fields:
            raise Exception("Fields are not initialized, can not generate rows")
            
        field_names = self.fields.names()

        for record in self.records():
            row = [record.get(field) for field in field_names]
            yield row

def build(**kwargs):
    return DataSource(**kwargs)
