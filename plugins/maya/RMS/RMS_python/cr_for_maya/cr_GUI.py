import pymel.all as pm

def setTextBoxText(tb):
    tb.text = pm.fileDialog()
    tb.insertText(tb.text)

def setAttrFromFileDialog(obj, attrname):
    text = pm.fileDialog()
    obj.setAttr(attrname, text)
