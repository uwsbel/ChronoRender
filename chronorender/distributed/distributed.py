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
    execpath    = ""
    execcall    = ""

    class JobDescriptor(object):
        def __init__(self):
            self.walltime = 60
            self.nodes    = 1
            self.name     = 'render'
            self.stdout   = None
            self.stderr   = None
            self.queue    = None
            self.email    = None
            self.range    = [0, 0]
            self.nodes    = 1
            self.ppn      = 1
            self.prog     = None
            self.id       = None
            self.done     = False
            self.wd       = ""

        def resolveAssets(self, assetman):
            return  []

    @staticmethod
    def getTypeName():
        return "distributed"

    def __init__(self, *args,  **kwargs):
        super(Distributed, self).__init__(*args, **kwargs)

        self._walltime    = self.getMember('walltime')
        self._nodes       = self.getMember('nodes')
        self._ppn         = self.getMember('ppn')
        self._queue       = self.getMember('queue')
        self._devicecmds  = self.getMember('devicecmds')
        self._execpath    = self.getMember('execpath')
        self._execcall    = self.getMember('execcall')

    def _initMembersDict(self):
        super(Distributed, self)._initMembersDict()

        self._members['walltime']   = [float, Distributed.walltime]
        self._members['nodes']      = [int, Distributed.nodes]
        self._members['ppn']        = [int, Distributed.ppn]
        self._members['queue']      = [str, Distributed.queue]
        self._members['devicecmds'] = [str, Distributed.devicecmds]
        self._members['execpath']   = [str, Distributed.execpath]
        self._members['execcall']   = [str, Distributed.execcall]

    def initialize(self):
        raise DistributedException('not implemented')

    def connect(self, server=None):
        raise DistributedException('not implemented')

    def createJobTemplate(self):
        job = Distributed.JobDescriptor()
        self._setJobDefaults(job)
        return job

    def finalizeJob(self, job, assetman):
        return

    def submit(self, job):
        raise DistributedException('not implemented')

    def wait(self, job, timeout):
        raise DistributedException('not implemented')

    def end(self):
        raise DistributedException('not implemented')

    def getConnection(self):
        raise DistributedException('not implemented')

    def _setJobDefaults(self, job):
        job.walltime  = self._walltime
        job.queue     = self._queue
        job.ppn       = self._ppn
        job.nodes     = self._nodes

def build(**kwargs):
    return Distributed(**kwargs)
