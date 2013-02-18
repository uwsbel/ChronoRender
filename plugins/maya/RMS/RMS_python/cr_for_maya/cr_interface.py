import os, sys, gc
import pymel.all as pm

import cr_Utils
import cr_for_maya.cr_loader as cr_loader
from MayaProjUtils import MayaProjUtils
from chronorender import ChronoRender
from chronorender.metadata import MDReaderFactory
from cr_Object import CRObject, CRObject_Node
from cr_Simulation import CRSimulation

_crHandle = CRObject_Node._root
_simHandle = "simulation"
_bRif = 0

Utils = MayaProjUtils()
SimRenderScript = 'cr_SimulationRI_Win' if sys.platform == 'win32' else 'cr_SimulationRI_Linux'
Factories = ChronoRender().getFactories()

gNodes = []

#==========================CMDS============================
def build(typename=None):
    _updateNodes()

    node = None
    if not typename or typename == CRSimulation.getTypeName():
        node = CRSimulation(Factories)
    gNodes.append(node)

def export():
    _export(sel())

def exportAll():
    _export(gNodes)

def _export(nodes):
    _updateNodes()

    os.chdir(Utils.getProjPath())
    cr_Utils.createOutDirs()
    path = cr_Utils.getOutPathFor('root')
    path = os.path.join(path, 'sim.yml')
    if os.path.exists(path):
        os.remove(path)

    md = MDReaderFactory.build(path)

    for obj in nodes:
        obj.export(md)

    md.writeToDisk()
    del md

def load(mdfile):
    _updateNodes()
    for obj in cr_loader.import_from_md(mdfile):
        gNodes.append(obj)

def edit():
    _updateNodes()

    nodes = sel()
    if len(nodes) > 0:
        window = nodes[0].createGUI()
        pm.showWindow(window)

def sel(addt_attr=None):
    _updateNodes()
    if not addt_attr:
        addt_attr = _crHandle

    out = []
    selected = pm.selected()
    for obj in gNodes:
        if _isSelected(obj, selected):
            out.append(obj)
    for obj in CRObject._gNodes:
        if _isSelected(obj, selected):
            out.append(obj)
    return out

def _isSelected(obj, selected):
    if obj.node in selected:
        return True
    if obj.node.getTransform() in selected:
        return True
    if obj.node.getShape() in selected:
        return True
    return False

def toggleRif():
    global _bRif
    if _bRif == 0: _bRif = 1
    else: _bRif = 0
    pm.mel.eval('rman setPref DisableRifShaderAttachment ' + str(_bRif))

def attachRIBArchive():
    _updateNodes()
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
    _updateNodes()
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
    _updateNodes()
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
        sim.setPreShapeScript(SimRenderScript)

def source():
  return

#==========================UTILS============================
def _updateNodes():
    global gNodes
    nodes = []
    for obj in gNodes:
        if obj.node: continue
        for parent, name in obj.parents.iteritems():
            parent.removeChild(obj)
        del obj
    for obj in CRObject._gNodes:
        if obj.node: continue
        for parent, name in obj.parents.iteritems():
            parent.removeChild(obj)
        del obj

    gNodes = [obj for obj in gNodes if obj.node]
    CRObject._gNodes = [obj for obj in CRObject._gNodes if obj.node]
    gc.collect()

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
os.chdir(Utils.getProjPath())
# disable rifs so can render without RMS
toggleRif()
