from distributedjob import DistributedManager

class PBSException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class PBS(DistributedManager):
    @staticmethod
    def getTypeName():
        return "pbs"

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
