from chronorender.renderpass.renderpass import RenderPass

class RayTracePass(RenderPass):

    @staticmethod
    def getTypeName():
        return "raytrace"

    def __init__(self, *args, **kwargs):
        super(RayTracePass,self).__init__(*args, **kwargs)

        self.bias = self.getMember('bias')

        self.addAttribute("visibility", {"int diffuse" : 1})
        self.addAttribute("visibility", {"int specular" : 1})
        self.addAttribute("visibility", {"int transmission" : 1})
        self.addAttribute("trace", {"float bias" : self.bias})

    def _initMembersDict(self):
        super(RayTracePass, self)._initMembersDict()
        self._members['bias'] = [float, 0.005]

def build(**kwargs):
    return RayTracePass(**kwargs)
