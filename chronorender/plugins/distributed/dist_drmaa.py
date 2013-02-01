from distributed import Distributed

import pbs

class DRMAAException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class DRMAA(Distributed):
    @staticmethod
    def getTypeName():
        return "pbs"

    def __init__(self, *args, **kwargs):
        super(DRMAA, self).__init__(*args, **kwargs)

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
      
def build(**kwargs):
    return DRMAA(**kwargs)
