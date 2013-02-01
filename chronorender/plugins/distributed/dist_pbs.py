from chronorender.distributed import Distributed

import pbs
import traceback, sys

class PBSException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PBS(Distributed):
    @staticmethod
    def getTypeName():
        return "pbs"

    def __init__(self, *args, **kwargs):
        super(PBS, self).__init__(*args, **kwargs)
        # stack = traceback.format_stack()
        # for s in stack:
          # print s
        self._connection_id = None

        self._name = self.getMember('name')

    def _initMembersDict(self):
        super(PBS, self)._initMembersDict()
        self._members['name']   = [str, '']

    def initialize(self, server=None):
        self.connect()

    def connect(self, server=None):
        if not server:
          server = pbs.pbs_default()
        self._connection_id = pbs.pbs_connect(server)

        if not self._connection_id:
            raise PBSException('could not connect to pbs server ' + str(server))

    def submit(self, job):
        print job

    def runJob(self, job):
        return None

    def runJobs(self, joblist):
        out = []
        for job in joblist:
            out.append(self.runJob(job))
        return out

    def wait(self, jobid, timeout):
        return

    def synchronize(self, timeout):
        return

    def end(self):
        if self._connection_id:
          pbs.pbs_disconnect(self._connection_id)
        self._connection_id = None

    def getConnection(self):
        return self._connection_id

    def _setJobDefaults(self, job):
        job.walltime  = Distributed.walltime
        job.queue = Distributed.queue
        job.ppn   = Distributed.ppn
        job.nodes = Distributed.nodes
        job.script = self._job2Script(job)

    def _job2Script(self, job):
        script = "#!/bin/bash\n"
        script += "#PBS -N " + str(job.name) + "\n"
        script += "#PBS -l nodes=" + str(job.nodes) + ":ppn=" + str(job.ppn) + "\n"
        script += "#PBS -t " + str(job.range[0]) + "-" + str(job.range[1]) + "\n"
        script += "#PBS -q " + str(job.queue) + "\n"
        script += "cd $PBS_O_WORKDIR"
        script += Distributed.devicecmds
        script += Distributed.exec_call
        return script

def build(**kwargs):
    obj = PBS(**kwargs)
    return obj
