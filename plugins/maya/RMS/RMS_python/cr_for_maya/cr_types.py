from cr_for_maya.cr_DataObject import CRDataObject
from cr_for_maya.cr_DataSource import CRDataSource
from cr_for_maya.cr_Geometry import CRGeometry
from cr_for_maya.cr_RenderObject import CRRenderObject
from cr_for_maya.cr_Shader import CRShader
from cr_for_maya.cr_Simulation import CRSimulation

# def init_type_dict():
    # return

#FIXME no hard code
type_dict = {
        CRDataObject.crtype.getTypeName() : CRDataObject,
        CRDataSource.crtype.getTypeName() : CRDataSource,
        CRGeometry.crtype.getTypeName() : CRGeometry,
        CRRenderObject.crtype.getTypeName() : CRRenderObject,
        CRShader.crtype.getTypeName() : CRShader,
        CRSimulation.crtype.getTypeName() : CRSimulation
        }
