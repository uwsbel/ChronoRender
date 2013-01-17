from cr_object import Object

import datasource as ds
import dataprocess as dp

class DataObject(Object):
    @staticmethod
    def getTypeName():
        return "data"

    def __init__(self, *args, **kwargs):
        super(DataObject, self).__init__(*args, **kwargs)

        self._datasrcs      = self.getMember(ds.DataSource.getTypeName())
        self._dataprocs     = self.getMember(dp.DataProcess.getTypeName())
        self._brun          = False

    def _initMembersDict(self):
        self._members[ds.DataSource.getTypeName()] = [list, []]
        self._members[dp.DataProcess.getTypeName()] = [list, []]

    def addDataSource(self, src):
        self._datasrcs.append(src)

    def addDataProcess(self, proc):
        self._dataprocs.append(proc)

    def run(self):
        self._brun = True
        return

    def getOutput(self):
        if not self._brun:
            self.run()
        out = []
        return out

def build(**kwargs):
    return DataObject(**kwargs)
