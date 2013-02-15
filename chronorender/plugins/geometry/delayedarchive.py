from chronorender.geometry import Geometry

class DelayedArchive(Geometry):
    @staticmethod
    def getTypeName():
        return "delayedarchive"

    def __init__(self, *args, **kwargs):
        super(DelayedArchive,self).__init__(*args, **kwargs)
        self.filename = self.getMember('filename')
        self.filepath = ""

    def _initMembersDict(self):
        super(DelayedArchive,self)._initMembersDict()
        self._members['filename'] = [str, '']

    def updateMembers(self):
        self.setMember('filename', self.filename)

    def resolveAssets(self, assetman):
        out = super(DelayedArchive, self).resolveAssets(assetman)
        # self.filepath = assetman.find(self.filename)
        # return [self.filename]
        return []

    def render(self, rib, *args, **kwargs):
        # rib.ReadArchive(self.filename)
        rib.Procedural(self.filename, [-1,1,-1,1,-1,1],
                rib.ProcDelayedReadArchive, rib.NULL)

def build(**kwargs):
    return DelayedArchive(**kwargs)
