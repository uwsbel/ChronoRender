from chronorender.geometry import Geometry
import os.path

class DelayedArchive(Geometry):

    _zippath = 'renderman/ribarchives/job/'

    @staticmethod
    def getTypeName():
        return "delayedarchive"

    def __init__(self, *args, **kwargs):
        super(DelayedArchive, self).__init__(*args, **kwargs)
        self.filename = self.getVar('filename', kwargs)
        self.filepath = ""
        self.zipped = self.getVar('zipped', kwargs)

    def _initMembersDict(self):
        super(DelayedArchive, self)._initMembersDict()
        self._members['filename'] = [str, '']
        self._members['zipped']   = [bool, True]

    def updateMembers(self):
        self.setMember('filename', self.filename)
        self.setMember('zipped', self.zipped)

    def resolveAssets(self, assetman):
        out = super(DelayedArchive, self).resolveAssets(assetman)
        # renderman wants linux paths
        self.filename = self.filename.replace('\\','/')
        # self.filepath = assetman.find(self.filename)
        # return [self.filename]
        return []

    def render(self, rib, *args, **kwargs):
        rib.Procedural(self._evalZippedPath(), [-1,1,-1,1,-1,1],
                rib.ProcDelayedReadArchive, rib.NULL)

    # want this pattern if zipped
    # ["renderman/ribarchives/pSphere1RibArchiveShape.zip!renderman/ribarchives/job/pSphere1RibArchiveShape.job.rib"]
    def _evalZippedPath(self):
        if not self.zipped:
            return self.filename

        toks = self.filename.split('!')
        if len(toks) == 2:
            return self.filename

        return self._appendZippedPath()

    def _appendZippedPath(self): 
        filename = os.path.split(self.filename)[1]
        f_noext = os.path.splitext(filename)[0]
        return self.filename + '!' + DelayedArchive._zippath + f_noext + '.job.rib'


def build(**kwargs):
    return DelayedArchive(**kwargs)
