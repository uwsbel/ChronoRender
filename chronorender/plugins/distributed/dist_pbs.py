from chronorender.distributed import Distributed

import pbs, sys

class PBSException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PBS(Distributed):
    @staticmethod
    def getTypeName():
        return "pbs"

    class PBSJobDescriptor(Distributed.JobDescriptor):
        def __init__(self):
          super(PBS.PBSJobDescriptor, self).__init__()
          self.script = ""

        def resolveAssets(self, assetman):
            print "SCRIPT", self.script
            return  [self._writeScriptToDisk(assetman)]

        def _writeScriptToDisk(self, assetman):
            filename = ''
            return filename

    def __init__(self, *args, **kwargs):
        super(PBS, self).__init__(*args, **kwargs)

        self._connection_id = None

    def _initMembersDict(self):
        super(PBS, self)._initMembersDict()

    def initialize(self, server=None):
        self.connect()

    def connect(self, server=None):
        if not server:
          server = pbs.pbs_default()
        self._connection_id = pbs.pbs_connect(server)

        if not self._connection_id:
            raise PBSException('could not connect to pbs server ' + str(server))

    def createJobTemplate(self):
        job = PBS.PBSJobDescriptor()
        self._setJobDefaults(job)
        return job

    def finalizeJob(self, job, assetman):
        job.script = self._job2Script(job)
        return job.resolveAssets(assetman)

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
        super(PBS, self)._setJobDefaults(job)

    def _job2Script(self, job):
        script = "#!/bin/bash\n"
        script += "#PBS -N " + str(job.name) + "\n"
        script += "#PBS -l nodes=" + str(job.nodes) + ":ppn=" + str(job.ppn) + "\n"
        script += "#PBS -t " + str(job.range[0]) + "-" + str(job.range[1]) + "\n"
        script += "#PBS -q " + str(job.queue) + "\n"
        script += "cd $PBS_O_WORKDIR\n"
        script += self._devicecmds
        script += self._getExportExecPathCMD()
        script += self._execcall
        return script

    def _getExportExecPathCMD(self):
        out = ""
        # platform = sys.platform
        # if platform == 'win32': 
        # else: 
        out = "export PATH=$PATH:" + self._execpath
        return out

    def resolveAssets(self, assetman):
        self._resolvedAssetPaths = True
        return  []

def build(**kwargs):
    obj = PBS(**kwargs)
    return obj
