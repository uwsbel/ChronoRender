from cr_object import Object
import cr_utils

import data
import datasource as ds
import dataprocess as dp
import datatarget as dt
import copy

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
        self._allfields     = []
        self._currindex     = 0
        self._maxindex      = 0

        self._initMultipleSourceResources()
        self._initCrossSrcFields()
 
    def _initMembersDict(self):
        self._members[ds.DataSource.getTypeName()] = [ds.DataSource, []]
        self._members[dp.DataProcess.getTypeName()] = [dp.DataProcess, []]

    def _initMultipleSourceResources(self):
        for i in range(0, len(self._datasrcs)):
            src = self._datasrcs[i]

            resources = src.getInputResources()
            resources = cr_utils.natural_sort(resources)
            tmp_srcs = []
            for resource in resources:
                new_src = copy.deepcopy(src)
                new_src.resource = resource
                tmp_srcs.append(new_src)
            self._datasrcs[i] = tmp_srcs
            
            if len(tmp_srcs) > self._maxindex:
                self._maxindex = len(tmp_srcs)

    def addDataSource(self, src):
        self._datasrcs.append(src)

    def addDataProcess(self, proc):
        self._dataprocs.append(proc)

    def getData(self, srcnumber=-1, selectcondition=""):
        if srcnumber == -1:
            srcnumber = self._currindex
            self.incrDataSourceCounter()

        if srcnumber >= self._maxindex:
            return None


        out = self._run(srcnumber)
        if selectcondition != "":
            src= ds.RecordListSourceNode(name="tmp", a_list=out, 
                    fields=data.FieldList(self._allfields))
            procs = []
            procs.append(dp.SelectNode(condition=selectcondition))
            out = DataObject._doProcs(src, procs)
        return out

    def incrDataSourceCounter(self):
        self._currindex += 1

    def resetDataSourceCounter(self):
        self._currindex = 0

    def _initCrossSrcFields(self):
        for srclist in self._datasrcs:
            src = srclist[0]
            if hasattr(src, 'fields'):
                for field in src.fields:
                    if field not in self._allfields:
                        self._allfields.append(field)

    def _run(self, srcnumber):
        #####
        # TODO have procs for filtering each srd
        # data = src.runProcs()
        ####

        # append proc outputs
        if len(self._datasrcs) <= 0:
            return None

        if len(self._datasrcs) == 1:
            node = ds.DataSourceNode(self._getResource(0, srcnumber))
            return self._doProcs(node, self._dataprocs)

        combined_data = self._combineSrcs(srcnumber)

        target = ds.RecordListSourceNode(name="tmp", a_list=combined_data.data, fields=data.FieldList(self._allfields))
        return self._doProcs(target, self._dataprocs)

    def _getResource(self, listnum, number):
        srcs = self._datasrcs[listnum]
        if number >= len(srcs):
            return srcs[len(srcs)-1]
            # TODO PROGRAM LOGGER
            # raise DataObjectException("asking for " + str(number) + " when only" 
                    # + str(len(srcs)) + "available")
        elif number < 0:
            return srcs[0]
        return srcs[number]

    def _combineSrcs(self, srcnumber):
        target = dt.DataTarget()
        target.fields = data.FieldList(self._allfields)

        target.initialize()
        for i in range(0, len(self._datasrcs)):
            src = self._getResource(i, srcnumber)
            src.initialize()
            for record in src.records():
                target.append(record)
            src.finalize()
        target.finalize()
        return target


    @staticmethod
    def _doProcs(datasrcnode, procs):
        out = dt.DataTarget()
        nodes = {
                    "in" : datasrcnode,
                    "out" : out
                }

        connections = DataObject._createProcGraph(nodes, procs, "in","out")
        stream = data.Stream(nodes, connections)
        stream.run() 
        return out.data

    @staticmethod
    def _createProcGraph(nodes, procs, inname, outname):
        connections = [[inname, ""]]
        for i in range(0, len(procs)):
            proc = procs[i]
            nodes[proc.name] = proc
            connections[i][1] = proc.name
            connections.append([proc.name, ""])
        connections[len(connections)-1][1] = outname
        return connections

def build(**kwargs):
    return DataObject(**kwargs)

