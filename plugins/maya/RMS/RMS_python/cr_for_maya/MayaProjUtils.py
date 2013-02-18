import maya.cmds as mc
import os

# Malcolm Kesson
# Nov 5  2012
  
class MayaProjUtils():
    #-----------------------------------------
    def getSceneName(self):
        name = mc.file(q=True, sceneName=True, shortName=True)
        if len(name) == 0:
            name = 'untitled'
        else:
            name = name[:len(name) - 3]
        return name
    #-----------------------------------------
    def getProjPath(self):
        projpath = mc.workspace(q=True, rootDirectory=True)
        return projpath
    #-----------------------------------------
    def getDataPath(self):
        projpath = self.getProjPath()
        return projpath + 'data'
    #-----------------------------------------
    def getRIB_ArchivePath(self):
        projpath = self.getProjPath()
        return projpath + 'RIB_Archive'
    #-----------------------------------------
    def getRMSRoot(self):
        path = os.getenv('RMS_SCRIPT_PATHS')
        return os.path.dirname(path)
    #-----------------------------------------
    def getRMS_python(self):
        path = self.getRMSRoot()
        return path + '/RMS_python'
    #-----------------------------------------
    def getBeginFrame(self):
        if mc.getAttr('defaultRenderGlobals.animation') == 0:
            return int(mc.currentTime(q=True))
        else:
            return int(mc.getAttr('defaultRenderGlobals.startFrame'))
    #-----------------------------------------
    def getEndFrame(self):
        if mc.getAttr('defaultRenderGlobals.animation') == 0:
            return int(mc.currentTime(q=True))
        else:
            return int(mc.getAttr('defaultRenderGlobals.endFrame'))
    #-----------------------------------------
    def getCurrentTime(self):
        return int(mc.currentTime(q=True))
    #-----------------------------------------
    def getPadding(self, frame):
        return "%0*d" % (4, frame)
