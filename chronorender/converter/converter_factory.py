from objconverter import OBJConverter
from plyconverter import PLYConverter
from maconverter import MAConverter
from dddsconverter import DDDSConverter
import os.path as path


class ConverterFactoryException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ConverterFactory(object):
    @staticmethod
    def build(src):
        ext = path.splitext(src)[1]
        ext = str.lower(ext)

        if ext == ".obj":
            return OBJConverter(src)
        elif ext == ".ply":
            return PLYConverter(src)
        elif ext == ".ma":
            return MAConverter(src)
        elif ext == ".3ds":
            return DDDSConverter(src)

        raise ConverterFactoryException('unsupported filetype: ' +
                str(src))
