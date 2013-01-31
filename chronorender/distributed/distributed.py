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

class Distributed(object):
    queue = None

    @staticmethod
    def getTypeName():
        return "distributed"

    def __init__(self):
        return

    # if server == None, try default connection
    def initialize(self, server=None):
        return

    def createJobTemplate(self):
        job = JobDescriptor()
        job.queue = Distributed.queue
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

def build(**kwargs):
    return Distributed()
