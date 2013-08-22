from chronorender.renderpass import RenderPass
import os
import chronorender.shader as cs
import shutil

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
        frame_file_exists = False
        passargs = {'framenumber' : framenumber, 'outpath' : outpath}
        passargs = dict(passargs.items() + kwargs.items())

        rib.FrameBegin(framenumber)
        rib.PixelFilter("box", 1, 1)
        # Declare "shadowname" "uniform string"
        rib.Declare("shadowname", "uniform string")
        rib.Declare("sfpx", "uniform string")
        rib.Declare("sfpy", "uniform string")
        rib.Declare("sfpz", "uniform string")
        rib.Declare("sfnx", "uniform string")
        rib.Declare("sfny", "uniform string")
        rib.Declare("sfnz", "uniform string")
        self._renderSettings(rib, **passargs)

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
        light_name = self.lighting[0].filename[:-4]
        key_index = light_name.rfind("-")
        if key_index != -1:
            frame_file_exists = True
            light_name = light_name[:key_index]

        rib.WorldBegin()
        for obj in self.renderables:
            obj.render(rib, rendershaders=False, colorobject=False, framenumber=framenumber, **kwargs)
        for scene in self.scene:
            scene.render(rib, **kwargs)

        rib.WorldEnd()
        path = os.path.join(os.path.join(os.path.join(os.getcwd(), "job"), "images"), "{0}-{1}.shd".format(base_name, framenumber))
        rib.MakeShadow("./job/images/{0}.{1}.z".format(base_name, framenumber), path)
        rib.FrameEnd()

        #Now create a brand new lighting file for each frame...
        if not frame_file_exists:
            orig_file = os.path.join(os.getcwd(), self.lighting[0].filename)
            new_lighting_filename = "{0}-{1}.rib".format(light_name, framenumber)
            new_file = os.path.join(os.path.join(os.getcwd(), 'ribarchives'), new_lighting_filename)
            # new_file = os.path.join(os.getcwd(), new_lighting_filename)
            # shutil.copyfile(orig_file, new_file)

            fin = open(orig_file, 'r')
            fout = open(new_file, 'w')
            for line in fin:
                # if line.split(" ")[2] == self.name[-2:]:
                line = line.replace(".shd", "-{0}.shd".format(framenumber))

                fout.write(line)

            fin.close()
            fout.close()

            self.lighting[0].filename = new_lighting_filename


def build(**kwargs):
    return ShadowPass(**kwargs)
