from chronorender.renderpass import RenderPass
import os
import chronorender.shader as cs

class RenderPassException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class ShadowPass(RenderPass):

    @staticmethod
    def getTypeName():
        return "shadow"

    def __init__(self, *args, **kwargs):
        super(ShadowPass,self).__init__(*args, **kwargs)

    def _initMembersDict(self):
        super(ShadowPass,self)._initMembersDict()

    def resolveAssets(self, assetman):
        out = []
        out.append(self.rndrsettings[0]._params['shadowfilepath'])
        self._resolvedAssetPaths = True
        return out

    def render(self, rib, passnumber, framenumber, outpath, *args, **kwargs):

        passargs = {'framenumber' : framenumber, 'outpath' : outpath}
        passargs = dict(passargs.items() + kwargs.items())

        rib.FrameBegin(framenumber)
        self._renderSettings(rib, **passargs)

        rib.PixelFilter("box", 1, 1)
        # rib.BoxFilter("box",1, 1)
        rib.Hider("hidden", {"int jitter": 0}) #TODO: error?


        # rib.Display(outpath, "zfile", "z")

        self.renderAttributes(rib)

        params = self.rndrsettings[0]._params

        # for cam in self.camera:
            # cam.render(rib, **kwargs)

        # self._renderLighting(rib, **kwargs)

        # self._renderInstanceDecls(rib, **passargs)

        rib.ScreenWindow(-1, 1, -1, 1)

        # rib.ReadArchive("custom_camera.rib")
        rib.ReadArchive(self.rndrsettings[0]._params['shadowfilepath'])
        base_name = self.rndrsettings[0]._params['shadowfilepath'][:-4]

        rib.WorldBegin()
        # import pdb; pdb.set_trace()
        for obj in self.renderables:
            obj.render(rib, framenumber=framenumber, **kwargs)
        for scene in self.scene:
            scene.render(rib, **kwargs)

        rib.WorldEnd()
        path = os.path.join(os.path.join(os.path.join(os.getcwd(), "job"), "images"), "{0}.shd".format(base_name))
        rib.MakeShadow("./job/images/{0}.{1}.z".format(base_name, framenumber), path)
        rib.FrameEnd()

def build(**kwargs):
    return ShadowPass(**kwargs)
