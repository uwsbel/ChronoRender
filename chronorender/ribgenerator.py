import os
import StringIO

import chronorender.datasource as ds

class RIBGeneratorException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class RIBGenerator():

    # max in mem at give time
    _MaxBufferSize = 5000000

    def __init__(self, factories, md, *args, **kwargs):
        self._datadelim         = ","
        self._filename          = ""
        self._datapath          = "./"
        self._idcounter         = 0
        self._idindex           = -1
        self._buffersize        = 0
        self._rawdata           = []
        self._organizeddata     = {}
        self._bytesread         = 0

        self.initFromMetadata(md)

    def initFromMetadata(self, md):
        self.md = md

    def dumpRIBToFile(self, rndrobjs, filein, fileout):
        self.__initOrganizedDataMap(rndrobjs)
        while self.__readRawData(filein) != True:
            self.__organizeRawData(rndrobjs)
            out = self.__dumpToStringBuffer()
        f = open(fileout, 'w')
        f.write(out)

    def dumpRIBToStdOut(self, rndrobjs, filein):
        self.__initOrganizedDataMap(rndrobjs)
        while self.__readRawData(filein) != True:
            self.__organizeRawData(rndrobjs)
            out = self.__dumpToStringBuffer()
        # print(out)

    def __initOrganizedDataMap(self, rndrobjs):
        self._organizeddata.clear()
        for obj in rndrobjs:
            self._organizeddata[obj] = []

    def __readRawData(self, filein):
        if os.path.exists(filein) != True:
            raise RIBGeneratorException('could not find data file: ' + filein)

        filesize = os.path.getsize(filein)

        if self._bytesread == filesize:
            self._bytesread = 0
            return True

        if (filesize - self._bytesread) > RIBGenerator._MaxBufferSize:
            self.__slowFileRead(filein)
            self._bytesread += RIBGenerator._MaxBufferSize
        else:
            self.__fastFileRead(filein)
            self._bytesread = filesize

        return False


    def __fastFileRead(self, filein):
        f = open(filein, 'r')
        self._rawdata = f.readlines()
        f.close()


    def __slowFileRead(self, filein):
        raise RIBGeneratorException('file too big: ' + filein)
        f = open(filein, 'r')
        for line in f:
            self._bytesread += RIBGenerator._MaxBufferSize
        f.close()

    def __organizeRawData(self, rndrobjs):
        for entry in self._rawdata:
            splitdata = entry.split(self._datadelim)
            robj = self.__getRenderObjectInstance(rndrobjs, splitdata)
            self._organizeddata[robj].append(robj.parseData(splitdata))
            self._idcounter += 1

    def __getRenderObjectInstance(self, rndrobjs, data):
        return rndrobjs[0]

    def __dumpToStringBuffer(self):
        buff = StringIO.StringIO()

        for obj, entry in self._organizeddata.iteritems():
            buff.write(obj.render(entry))

        output = buff.getvalue()
        buff.close()
        return output
