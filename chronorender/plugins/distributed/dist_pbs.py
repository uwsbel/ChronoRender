from chronorender.distributed import Distributed

import pbs, sys, os

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
          self.scriptpath = ""

        def resolveAssets(self, assetman):
            self.scriptpath = self._writeScriptToDisk(assetman)
            return  [self.scriptpath]

        def _writeScriptToDisk(self, assetman):
            path = assetman.getOutPathFor('output')
            filename = os.path.join(path, self.name)
            filename += ".sh"
            f = open(filename, 'w')
            f.write(self.script)
            f.close()
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
        self._configureJobProg(job)
        job.script = self._job2Script(job)
        return job.resolveAssets(assetman)

    def submit(self, job):
        attr = self._job2AttrOp(job)
        jobid = pbs.pbs_submit(self._connection_id, attr,
            job.scriptpath, job.queue, "NULL")
        job.id = jobid

    def wait(self, job):
        if job.done:
            return
        status = self._getJobStatus(job.id)
        while status != "E":
            status = self._getJobStatus(job.id)
        job.done = True
        
    def end(self):
        if self._connection_id:
          pbs.pbs_disconnect(self._connection_id)
        self._connection_id = None

    def getConnection(self):
        return self._connection_id

    def _setJobDefaults(self, job):
        super(PBS, self)._setJobDefaults(job)
        job.wd = "$PBS_OWORKDIR"

    def _configureJobProg(self, job):
        job.prog.args['framerange'] = '$PBS_ARRAYID $PBS_ARRAYID'

    def _getJobStatus(self, jobid):
        status = pbs.pbs_statjob(self._connection_id, jobid, "NULL", "NULL")
        job_state = status[0].attribs
        for attr in job_state:
            if attr.name == "job_state":
                return attr.value

    def _job2Script(self, job):
        script = "#!/bin/bash\n"
        # script += "#PBS -N " + str(job.name) + "\n"
        # script += "#PBS -l nodes=" + str(job.nodes) + ":ppn=" + str(job.ppn) + "\n"
        # script += "#PBS -t " + str(job.range[0]) + "-" + str(job.range[1]) + "\n"
        # script += "#PBS -q " + str(job.queue) + "\n"
        # script += "cd $PBS_OWORKDIR\n"
        script += "cd " + job.wd + "\n"
        script += self._devicecmds +"\n"
        script += self._getExportExecPath(job.prog) + "\n"
        script += job.prog.getProgCall()
        return script

    def _job2AttrOp(self, job):
        attr = pbs.new_attropl(4)
        attr[0].name      = pbs.ATTR_N
        attr[0].value     = job.name

        attr[1].name      = pbs.ATTR_l
        attr[1].resource  = 'walltime'
        attr[1].value     = str(job.walltime)

        attr[2].name      = pbs.ATTR_l
        attr[2].resource  = 'nodes'
        attr[2].value     = str(job.nodes) + ":ppn=" + str(job.ppn)

        attr[3].name      = pbs.ATTR_t
        attr[3].value     = str(job.range[0]) + "-" + str(job.range[1])
        return attr

    def _getExportExecPath(self, prog):
        out = ""
        # platform = sys.platform
        # if platform == 'win32': 
        # else: 
        out = "export PATH=$PATH:" + prog.path
        return out

    def resolveAssets(self, assetman):
        self._resolvedAssetPaths = True
        return  []

def build(**kwargs):
    obj = PBS(**kwargs)
    return obj
