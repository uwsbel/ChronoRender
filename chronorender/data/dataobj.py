from cr_object import Object

import data
import datasource as ds
import dataprocess as dp
import datatarget as dt


class DataObjectException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DataObject(Object):
    @staticmethod
    def getTypeName():
        return "data"

    def __init__(self, *args, **kwargs):
        super(DataObject, self).__init__(*args, **kwargs)

        self._datasrcs      = self.getMember(ds.DataSource.getTypeName())
        self._dataprocs     = self.getMember(dp.DataProcess.getTypeName())
 
    def _initMembersDict(self):
        self._members[ds.DataSource.getTypeName()] = [ds.DataSource, []]
        self._members[dp.DataProcess.getTypeName()] = [dp.DataProcess, []]

    def addDataSource(self, src):
        self._datasrcs.append(src)

    def addDataProcess(self, proc):
        self._dataprocs.append(proc)

    def getData(self):
        return self.run()

    def run(self):
        #####
        # TODO have procs for filtering each srd
        # data = src.runProcs()
        ####

        # append proc outputs
        if len(self._datasrcs) <= 0:
            return None

        if len(self._datasrcs) == 1:
            return self._doProcs(ds.DataSourceNode(self._datasrcs[0]))

        fields, combined_data = self._combineSrcs()

        target = ds.RecordListSourceNode(name="tmp", a_list=combined_data.data, fields=fields)
        return self._doProcs(target)

    def _combineSrcs(self):
        all_fields = data.FieldList(["file"])
        for src in self._datasrcs:
            for field in src.fields:
                if field not in all_fields:
                    all_fields.append(field)
        target = dt.DataTarget()
        target.fields = data.FieldList(all_fields)

        target.initialize()
        for src in self._datasrcs:
            src.initialize()
            for record in src.records():
                target.append(record)
            src.finalize()
        target.finalize()
        return all_fields, target


    def _doProcs(self, datasrcnode):
        out = dt.DataTarget()
        nodes = {
                    "in" : datasrcnode,
                    "out" : out
                }

        connections = self._createProcGraph(nodes, "in","out")
        stream = data.Stream(nodes, connections)
        stream.run() 
        return out.data

    def _createProcGraph(self, nodes, inname, outname):
        connections = [[inname, ""]]
        for i in range(0, len(self._dataprocs)):
            proc = self._dataprocs[i]
            nodes[proc.name] = proc
            connections[i][1] = proc.name
            connections.append([proc.name, ""])
        connections[len(connections)-1][1] = outname
        return connections

def build(**kwargs):
    return DataObject(**kwargs)

