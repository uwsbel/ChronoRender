import pymel.all as pm
import os.path

import MayaProjUtils as mpu
import cr_for_maya.cr_Utils as crutils

def setTextBoxText(tb):
    tb.text = pm.fileDialog()
    tb.insertText(tb.text)

def setAttrFromFileDialog(obj, attrname):
    # get the relative path to project
    mutil = mpu.MayaProjUtils()
    projpath = mutil.getProjPath()

    text = pm.fileDialog()
    path = os.path.relpath(text, projpath)
    path = crutils.normalizePath(path)

    obj.setAttr(attrname, path)
