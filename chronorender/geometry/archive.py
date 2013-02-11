from chronorender.geometry import Geometry

class Archive(Geometry):
    @staticmethod
    def getTypeName():
        return "archive"

    def __init__(self, *args, **kwargs):
        super(Archive,self).__init__(*args, **kwargs)
        self.filename = self.getMember('filename')
        self.filepath = ""

    def _initMembersDict(self):
        super(Archive,self)._initMembersDict()
        self._members['filename'] = [str, '']

    def updateMembers(self):
        self.setMember('filename', self.filename)

    def resolveAssets(self, assetman):
        out = super(Archive, self).resolveAssets(assetman)
        # self.filepath = assetman.find(self.filename)
        return [self.filename]

    def render(self, rib, *args, **kwargs):
        rib.ReadArchive(self.filename)

def build(**kwargs):
    return Archive(**kwargs)
