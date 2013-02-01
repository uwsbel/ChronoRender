from chronorender.cr_object import Object
# push jobs to distributed manager
class DistributedException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Distributed(Object):
    walltime    = 60
    queue       = None
    ppn         = 32
    nodes       = 1
    devicecmds  = ""
    exec_path   = ""
    exec_call   = ""

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

    @staticmethod
    def getTypeName():
        return "distributed"

    def __init__(self, *args,  **kwargs):
        super(Distributed, self).__init__(*args, **kwargs)

    def _initMembersDict(self):
        super(Distributed, self)._initMembersDict()

    def initialize(self, server=None):
        raise DistributedException('not implemented')

    def createJobTemplate(self):
        job = Distributed.JobDescriptor()
        self._setJobDefaults(job)
        return job

    def submit(self, job):
        raise DistributedException('not implemented')

    def runJob(self, job):
        raise DistributedException('not implemented')

    def wait(self, jobid, timeout):
        raise DistributedException('not implemented')

    def synchronize(self, timeout):
        raise DistributedException('not implemented')

    def end(self):
        raise DistributedException('not implemented')

    def getConnection(self):
        raise DistributedException('not implemented')

    def _setJobDefaults(self, job):
        job.walltime  = Distributed.walltime
        job.queue = Distributed.queue
        job.ppn   = Distributed.ppn
        job.nodes = Distributed.nodes

def build(**kwargs):
    return Distributed(**kwargs)
