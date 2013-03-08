import os
import chronorender.cr_types as cr_types
from chronorender.cr_assetinfo import CRAssetInfo
from MayaProjUtils import MayaProjUtils

Utils = MayaProjUtils()

def crType2Maya(typ):
    if typ == str or typ == cr_types.url:
        return 'string'
    elif typ == float:
        return 'float'
    elif typ == bool:
        return 'bool'
    elif typ == list:
        return
    else:
        return None

def createOutDirs():
    assetman = CRAssetInfo( outpath=os.path.join(Utils.getProjPath(), 'renderman'), 
            jobname=Utils.getSceneName(), relative=False)
    assetman.createOutDirs()

def getOutPathFor(what):
    assetman = CRAssetInfo( outpath=os.path.join(Utils.getProjPath(), 'renderman'), 
            jobname=Utils.getSceneName(), relative=False)
    return assetman.getOutPathFor(what)

def normalizePath(path):
    return path.replace("\\", "/")
