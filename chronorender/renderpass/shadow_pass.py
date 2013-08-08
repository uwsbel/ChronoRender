from chronorender.renderpass.renderpass import RenderPass

class ShadowPass(RenderPass):

    @staticmethod
    def getTypeName():
        return "shadowpass"

    def __init__(self, *args, **kwargs):
        # super(ShadowPass,self).__init__(*args, **kwargs)

        self.addAttribute("death" {"int 0" : 0})

def build(**kwargs):
    return RayTracePass(**kwargs)
