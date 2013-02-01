# push jobs to distributed manager
class DistributedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class JobDescriptor(object):
    def __init__(self):
        self.walltime = 60
        self.nodes    = 1
        self.name     = 'render'
        self.stdout   = None
        self.stderr   = None
        self.queue    = None
        self.email    = None
        self.range    = [-1, -1]
        self.script   = ""
        self.nodes    = 1
        self.ppn      = 1

class Distributed(object):
    walltime    = 60
    queue       = None
    ppn         = 32
    nodes       = 1
    devicecmds  = ""
    exec_path   = ""
    exec_call   = ""

    @staticmethod
    def getTypeName():
        return "distributed"

    def __init__(self, **kwargs):
        return

    # if server == None, try default connection
    def initialize(self, server=None):
        return

    def createJobTemplate(self):
        job = JobDescriptor()
        self._setJobDefaults(job)
        return job

    def submit(self, job):
        return None

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
        return

    def getConnection(self):
        return None

    def _setJobDefaults(self, job):
        job.walltime  = Distributed.walltime
        job.queue = Distributed.queue
        job.ppn   = Distributed.ppn
        job.nodes = Distributed.nodes

def build(**kwargs):
    return Distributed()
