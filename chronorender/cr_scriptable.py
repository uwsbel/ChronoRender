from cr_object import Renderable

class Scriptable(Renderable):
    def __init__(self):
        super(Scriptable,self).__init__(*args, **kwargs)

        self._scriptname = self.getMember('script')
        self._func  = None

    def _initMembersDict(self):
        self._members['script']   = [str, '']

    def resolveAssets(self, finder):
        self._resolvedAssetPaths = True
        return []

    def setAsset(self, assetname, obj):
        return

    def render(self, rib, *args, **kwargs):
        return
