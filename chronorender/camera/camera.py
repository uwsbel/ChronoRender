from chronorender.cr_movable import Movable
from chronorender.cr_scriptable import Scriptable

class Camera(Movable):
    @staticmethod
    def getTypeName():
        return "camera"

    def getBaseName(self):
        return Camera.getTypeName()

    def __init__(self, *args, **kwargs):
        super(Camera,self).__init__(*args, **kwargs)

        self.filename   = self.getMember('filename')
        self.script     = self.getMember(Scriptable.getTypeName())
        self.moving_camera = self.getMember('moving_camera')

    def _initMembersDict(self):
        super(Camera, self)._initMembersDict()
        self._members['filename']   = [str, '']
        self._members[Scriptable.getTypeName()] = [Scriptable, None]
        self._members['moving_camera'] = [bool, True]

    def updateMembers(self):
        super(Camera, self).updateMembers()
        self.setMember('filename', self.filename)
        self.setMember(Scriptable.getTypeName(), self.script)

    def resolveAssets(self, assetman):
        out = []
        if self.script:
            out.extend(self.script.resolveAssets(assetman))
        elif self.filename != '':
            out.append(assetman.find(self.filename))
        self._resolvedAssetPaths = True
        return out

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, frame=None, *args, **kwargs):
        # import pdb; pdb.set_trace()
        if self.script:
            self.script.render(rib, *args, **kwargs)
        elif self.moving_camera:
            filename = self.filename.strip(".rib")
            filename = filename + "_{0}.rib".format(frame)
            rib.ReadArchive(filename)
            
        elif self.filename != '':
            rib.ReadArchive(self.filename)

def build(**kwargs):
    return Camera(**kwargs)
