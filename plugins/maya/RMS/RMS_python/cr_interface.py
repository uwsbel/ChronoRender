import os, sys
import pymel.all as pm
from MayaProjUtils import MayaProjUtils
from chronorender.cr_assetinfo import CRAssetInfo
from chronorender.metadata import MDReaderFactory

_crHandle = "chronorender"
_simHandle = "simulation"
_bRif = 0
utils = MayaProjUtils()
simRenderScript = 'cr_SimulationRI_Win' if sys.platform == 'win32' else 'cr_SimulationRI_Linux'

#==========================CMDS============================
def export():
    os.chdir(utils.getProjPath())

    createOutDirs()
    path = getOutPathFor('root')
    path = os.path.join(path, 'sim.yml')
    if os.path.exists(path):
        os.remove(path)
    md = MDReaderFactory.build(path)

    nodes = _getAndVerifyByAttr('export')
    for node in nodes:
        node.export(md)

    md.writeToDisk()
    del md

def edit():
    nodes = _getAndVerifyByAttr('createGUI')
    for node in nodes:
        window = node.createGUI()
        pm.showWindow(window)

def toggleRif():
    global _bRif
    if _bRif == 0: _bRif = 1
    else: _bRif = 0
    pm.mel.eval('rman setPref DisableRifShaderAttachment ' + str(_bRif))

def attachRIBArchive():
    nodes = _getAndVerifyByAttr('attachMesh')
    select = pm.selected()
    archives = []
    for sel in select:
        if sel.hasAttr('filename'):
            archives.append(sel)

    if len(archives) != 1:
        raise Exception('not 1 RIBArchive selected')

    for node in nodes:
        node.attachRIBArchive(archives[0])

def attachMesh():
    nodes = _getAndVerifyByAttr('attachMesh')
    nodemeshs = _getAndVerifyByType('mesh')

    # get the mesh
    meshes = []
    for mesh in nodemeshs:
        if mesh not in nodes:
            meshes.append(mesh)

    if len(meshes) != 1:
        raise Exception('not only 1 geometry node selected')

    for node in nodes:
        node.attachMesh(mesh)

def batchRI(platform):
    script = 'cr_SimulationRI_Win'
    if platform == 'posix':
      script = 'cr_SimulationRI_Linux'

    sims = _getNodesByAttr(pm.ls(), _simHandle)
    for sim in sims:
        tmp = sim.getPreShapeScript()
        sim.setPreShapeScript(script)
        print "script", tmp, sim.getPreShapeScript(), platform

    pm.mel.eval('batchRenderRI("", 1)')

    for sim in sims:
        sim.setPreShapeScript(simRenderScript)

def source():
  return

#==========================UTILS============================

def getSelected(addt_attr=None):
    if not addt_attr:
        addt_attr = _crHandle
    out = []
    all_nodes = getAllNodes()
    for node in all_nodes:
        if node.hasAttr(addt_attr):
            out.append(node)
    return out

def getAllNodes():
    selected = pm.selected()
    nodes = []
    for node in selected:
        nodes.extend(_conglomerateNodes(node))
    return nodes

def _conglomerateNodes(node):
    out = []
    if hasattr(node, 'listRelatives'):
        relatives = node.listRelatives()
        out.extend(relatives)
        for node in relatives:
            out.extend(_conglomerateNodes(node))
    out.extend(node.listConnections())
    return list(set(out))

def addRootHandle(node):
    node.addAttr(_crHandle, dt='string', h=True)

def createOutDirs():
    assetman = CRAssetInfo( outpath=os.path.join(utils.getProjPath(), 'renderman'), jobname=utils.getSceneName(), relative=False)
    assetman.createOutDirs()

def getOutPathFor(what):
    assetman = CRAssetInfo( outpath=os.path.join(utils.getProjPath(), 'renderman'), jobname=utils.getSceneName(), relative=False)
    return assetman.getOutPathFor(what)

def getMesh(node):
    inMesh = node.listConnections()
    for m in inMesh:
        if m.hasAttr('outMesh'):
            return m
    return None

def _getAndVerifyByAttr(attr):
    # nodes = _getNodesByAttr(getSelected(_crHandle), attr)
    nodes = _getNodesByAttr(getAllNodes(), attr)
    if len(nodes) == 0:
        raise Exception('no nodes selected that can ' + attr)
    return nodes

def _getAndVerifyByType(nodetype):
    nodes = _getNodesByType(getAllNodes(), nodetype)
    if len(nodes) == 0:
        raise Exception('no nodes selected with type ' + nodetype)
    return nodes

def _getNodesByAttr(nodes, attr):
    expnodes = [exp for exp in nodes if hasattr(exp, attr)]
    return expnodes

def _getNodesByType(nodes, nodetype):
    expnodes = [exp for exp in nodes if pm.nodeType(exp) == nodetype]
    return expnodes

# set working dir to project path to handle relative paths
os.chdir(utils.getProjPath())
# disable rifs so can render without RMS
toggleRif()
