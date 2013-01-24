from renderpass import RenderPass

class RayTracePass(RenderPass):

    @staticmethod
    def getTypeName():
        return "raytrace"

    def __init__(self, *args, **kwargs):
        super(RayTracePass,self).__init__(*args, **kwargs)

        self.bias = self.getMember('bias')

        self.addAttribute("visibility", {"int diffuse" : 1})
        self.addAttribute("visibility", {"int specular" : 1})
        self.addAttribute("trace", {"float bias" : self.bias})

    def _initMembersDict(self):
        super(RayTracePass, self)._initMembersDict()

        self._members['bias'] = [float, 0.005]

    def render(self, rib, passnumber, framenumber, outpath, *args, **kwargs):
        super(RayTracePass, self).render(rib, 
            passnumber, framenumber, outpath,
            *args, **kwargs)
        # if self.script:
            # self.script.render(rib, *args, **kwargs)
        # else:
            # rib.RiFrameBegin(passnumber)
            # for sett in self.rndrsettings:
                # sett.render(rib, outpath, **kwargs)

            # self.renderAttributes(rib)

            # self._renderInstanceDecls(rib, framenumber=framenumber, **kwargs)

            # for cam in self.camera:
                # cam.render(rib, **kwargs)

            # rib.RiWorldBegin()
            # for light in self.lighting:
                # light.render(rib, **kwargs)
            # for obj in self.renderables:
                # obj.render(rib, framenumber=framenumber, **kwargs)
            # for scene in self.scene:
                # scene.render(rib, **kwargs)
            # rib.RiWorldEnd()

            # rib.RiFrameEnd()


def build(**kwargs):
    return RayTracePass(**kwargs)
