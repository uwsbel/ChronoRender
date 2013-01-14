import os
from _mdxml import _MDXML
from _mdyaml import _MDYAML

class MDReaderFactory():
    def __init__():
        return

    @staticmethod
    def build(infile):
        ext = os.path.splitext(infile)[1]
        if ext == '.xml':
            return _MDXML(infile)
        elif ext == '.yaml':
            return _MDYAML(infile)
