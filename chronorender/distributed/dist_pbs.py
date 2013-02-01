from distributed import Distributed

import pbs

class PBSException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PBS(Distributed):
    @staticmethod
    def getTypeName():
        return "pbs"

    def __init__(self, **kwargs):
        self._connection_id = None

    def initialize(self, server=None):
        if not server:
          server = pbs.pbs_default()
        self._connection_id = pbs.pbs_connect(server)

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

    def _job2Script(self, job):
        script = "#!/bin/bash\n"
        script += "#PBS -N " + str(job.name) + "\n"
        script += "#PBS -l nodes=" + str(job.nodes) + ":ppn=" + str(job.ppn) + "\n"
        script += "#PBS -t " + str(job.range[0]) + "-" + str(job.range[1]) + "\n"
        script += "#PBS -q " + str(job.queue) + "\n"
        script += "cd $PBS_O_WORKDIR"
        script += Distributed.devicecmds
        script += Distributed.exec_call
