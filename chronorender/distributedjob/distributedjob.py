# push jobs to distributed manager
class DistributedManagerException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DistributedManager():
    @staticmethod
    def getTypeName():
        return "distribman"

    def __init__(self):
        return

    def initialize(self, server):
        return

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
