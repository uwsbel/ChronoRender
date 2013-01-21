import sys, types, time, os, os.path, string, getpass, inspect, gzip, cStringIO
from rib_stream import RIBStream
from ri_constants import *
from ri_types import *
from ri_error import *
import ri_utils as riutils

class RiStream():
    def __init__(self, name):
        self._colorsamples  = 3
        self._lighthandle   = 0
        self._errorhandler  = RiErrorPrint
        self._insideframe   = 0
        self._insideworld   = 0
        self._insideobject  = 0
        self._insidesolid   = 0
        self._insidemotion  = 0
        self._declarations = {}

        # Determine where the output should be directed to...
        if name==RI_NULL or name=="":
            # -> stdout
            outstream = sys.stdout
        elif name=="str":
            outstream = cStringIO.StringIO()
        else:
            root, ext = os.path.splitext(name)
            ext=ext.lower()
            if ext==".rib":
                # -> file (rib)
                outstream = open(name,"w")
            elif ext==".gz":
                outstream = gzip.open(name,"wb")
            else:
                # -> pipe
                outstream = os.popen(name,"w")

        self._ribout = RIBStream(outstream, name)
        self._current_context = None
        self._contexts = None
        self._objecthandle = 0

        self._init_declarations()

    def write(self, data):
        self._ribout.write(data)

    def getText(self):
        return self._ribout.getText()

    # RiErrorHandler
    def RiErrorHandler(self, handler):
        """Install a new error handler.

        The handler takes three arguments: code, severity, message.
        Besides the three standard error handler RiErrorIgnore, RiErrorPrint
        and RiErrorAbort there's an additional error handler available called
        RiErrorException. Whenever an error occurs RiErrorException raises
        the exception RIException.

        If you use one of the standard error handlers the corresponding RIB
        request is written to the output. If you supply RiErrorException or
        your own handler then the handler is installed but no output is
        written to the output stream.

        The last error code is always stored in the variable RiLastError.
        Note: If you import the module with "from ri import *" you have to
        import it with "import ri" as well and you must access RiLastError
        via "ri.RiLastError" otherwise the variable will always be 0.

        Example: RiErrorHandler(RiErrorAbort)
        """

        self._errorhandler = handler

        if handler==RiErrorIgnore:
            self._ribout.write('ErrorHandler "ignore"\n')
        elif handler==RiErrorPrint:
            self._ribout.write('ErrorHandler "print"\n')
        elif handler==RiErrorAbort:
            self._ribout.write('ErrorHandler "abort"\n')


    # RiBegin
    def RiBegin(self, name):
        """Starts the main block using a particular rendering method.
        
        The default renderer is selected by passing RI_NULL as name.
        Here this means the output is written to stdout.
        If the name has the extension ".rib" then the output is written into
        a file with that name. Otherwise the name is supposed to be an
        external renderer (e.g. "rendrib" (BMRT), "rgl" (BMRT), "aqsis" (Aqsis),
        "renderdl" (3Delight),...) which is started and fed with the data.

        Example: RiBegin(RI_NULL)
                 ...
                 RiEnd()
        """

        self._create_new_context()

    # RiEnd
    def RiEnd(self):
        """Terminates the main block.
        """

        self._ribout.flush()
        
        if self._ribout != sys.stdout:
            self._ribout.close()
            self._ribout = sys.stdout

        self._destroy_context()

    # RiWorldBegin
    def RiWorldBegin(self):
        """Start the world block.

        Example: RiWorldBegin()
                 ...
                 RiWorldEnd()
        """


        if self._insideworld:
            self._error(RIE_ILLSTATE, RIE_ERROR, "World blocks cannot be nested.")
        
        self._ribout.write("WorldBegin\n")
        self._insideworld = 1

    # RiWorldEnd
    def RiWorldEnd(self):
        """Terminates the world block."""

        
        self._ribout.write("WorldEnd\n")
        self._insideworld = 0

    # RiOption
    def RiOption(self, name, *paramlist, **keyparams):
        """Set an implementation-specific option.

        Example: RiOption("searchpath", "shader","~/shaders:&")
        """

        # cgkit specific options?
        if name==RI_RIBOUTPUT:
            keyparams = riutils.paramlist2lut(paramlist, keyparams)
            if keyparams.get(RI_VERSION, None)==0:
                # Disable the "version" call in the RIB stream...
                if hasattr(self._ribout, "output_version"):
                    self._ribout.output_version = 0
            return
                
        self._ribout.write('Option "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiAttribute
    def RiAttribute(self, name, *paramlist, **keyparams):
        """Set an implementation-specific attribute.

        Example: RiAttribute("displacementbound", "sphere", 0.5)
        """
        
        self._ribout.write('Attribute "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiAttributeBegin
    def RiAttributeBegin(self):
        """Push the current set of attributes onto the attribute stack.

        Example: RiAttributeBegin()
                 ...
                 RiAttributeEnd()
        """
        
        self._ribout.write("AttributeBegin\n")

    # RiAttributeEnd
    def RiAttributeEnd(self):
        """Pops the current set of attributes from the attribute stack."""

        self._ribout.write("AttributeEnd\n")

    # RiTransformBegin
    def RiTransformBegin(self):
        """Push the current transformation on the transformation stack.

        Example: RiTransformBegin()
                 ...
                 RiTransformEnd()
        """
        
        self._ribout.write("TransformBegin\n")

    # RiTransformEnd
    def RiTransformEnd(self):
        """Pop the current transformation from the stack."""

        self._ribout.write("TransformEnd\n")

    # RiFrameBegin
    def RiFrameBegin(self,number):
        """Start a new frame.

        Example: RiFrameBegin(1)
                 ...
                 RiFrameEnd()
        """


        if self._insideframe:
            self._error(RIE_ILLSTATE, RIE_ERROR, "Frame blocks cannot be nested.")
                
        self._ribout.write("FrameBegin %d\n"%number)
        self._insideframe = 1
        

    # RiFrameEnd
    def RiFrameEnd(self):
        """Terminates a frame."""
        
        
        self._ribout.write("FrameEnd\n")
        self._insideframe = 0

    # RiHider
    def RiHider(self, type, *paramlist, **keyparams):
        """Choose a hidden-surface elimination technique.

        Example: RiHider(RI_HIDDEN)  (default)
        """
        
        if type==RI_NULL: type="null"
        self._ribout.write('Hider "'+type+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiSphere
    def RiSphere(self, radius,zmin,zmax,thetamax,*paramlist, **keyparams):
        """Create a sphere.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiSphere(1.0, -1.0, 1.0, 360)
        """

        self._ribout.write('Sphere %s %s %s %s'%(radius, zmin, zmax, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiCone
    def RiCone(self, height, radius, thetamax, *paramlist, **keyparams):
        """Create a cone (along the z axis).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiCone(1.5, 0.7, 360)
        """

        self._ribout.write('Cone %s %s %s'%(height, radius, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiDisk
    def RiDisk(self, height, radius, thetamax, *paramlist, **keyparams):
        """Create a disk (parallel to the XY plane).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiDisk(0.0, 1.0, 360)"""

        self._ribout.write('Disk %s %s %s'%(height, radius, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiCylinder
    def RiCylinder(self, radius,zmin,zmax,thetamax,*paramlist, **keyparams):
        """Create a cylinder (along the z axis).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiCylinder(1.5, 0.0, 1.0, 360)
        """

        self._ribout.write('Cylinder %s %s %s %s'%(radius, zmin, zmax, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiTorus
    def RiTorus(self, major, minor, phimin, phimax, thetamax, *paramlist, **keyparams):
        """Create a torus (with the z axis as symmetry axis).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiTorus(1.5, 0.1, 0, 360, 360)
        """

        self._ribout.write('Torus %s %s %s %s %s'%(major, minor, phimin, phimax, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiHyperboloid
    def RiHyperboloid(self, point1, point2, thetamax, *paramlist, **keyparams):
        """Create a hyperboloid (with the z axis as symmetry axis).

        Example: RiHyperboloid([1,0,0],[1,1,1],360)
        """

        p1 = riutils.seq2list(self, point1, 3)
        p2 = riutils.seq2list(self, point2, 3)
        self._ribout.write('Hyperboloid '+p1[1:-1]+' '+p2[1:-1]+' '+`thetamax`+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiParaboloid
    def RiParaboloid(self, rmax, zmin, zmax, thetamax, *paramlist, **keyparams):
        """Create a paraboloid (with the z axis as symmetry axis).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4

        Example: RiParaboloid(1.0, 0.0, 1.0, 360)
        """

        self._ribout.write('Paraboloid %s %s %s %s'%(rmax, zmin, zmax, thetamax)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiPolygon
    def RiPolygon(self, *paramlist, **keyparams):
        """Create a planar and convex polygon.

        The parameter list must include at least position ("P") information.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #vertices
        uniform:  1              vertex:  #vertices

        Example: RiPolygon(P=[0,1,0, 0,1,1, 0,0,1, 0,0,0])
        """

        self._ribout.write('Polygon'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiGeneralPolygon
    def RiGeneralPolygon(self, nverts, *paramlist, **keyparams):
        """Create a general planar concave polygon with holes.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #total vertices
        uniform:  1              vertex:  #total vertices

        Example: RiGeneralPolygon([4,3], P=[0,0,0, 0,1,0, 0,1,1, 0,0,1, \\
                                            0,0.25,0.5, 0,0.75,0.75, 0,0.75,0.25])
        """

        self._ribout.write('GeneralPolygon '+ riutils.seq2list(self, nverts)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiPointsPolygons
    def RiPointsPolygons(self, nverts, vertids, *paramlist, **keyparams):
        """Create a polyhedron made of planar convex polygons that share vertices.

        nverts:  An array with the number of vertices in each polygon
        vertids: The vertex indices of the polygon vertices (0-based)
        The vertices themselves are stored in the parameter list (parameter "P").

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #vertices (*)
        uniform:  #polygons      vertex:  #vertices (*)

        (*) max(vertids)+1
        """

        self._ribout.write('PointsPolygons '+ riutils.seq2list(self, nverts)+' '+ \
                     riutils.seq2list(self, vertids)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiPointsGeneralPolygons
    def RiPointsGeneralPolygons(self, nloops, nverts, vertids, *paramlist, **keyparams):
        """Create a polyhedron made of general planar concave polygons.

        nloops:  The number of loops for each polygon
        nverts:  The number of vertices in each loop
        vertids: The vertex indices of the loop vertices (0-based)
        The vertices themselves are stored in the parameter list (parameter "P").

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #vertices (*)
        uniform:  #polygons      vertex:  #vertices (*)

        (*) max(vertids)+1
        """

        self._ribout.write('PointsGeneralPolygons '+riutils.seq2list(self, nloops)+' '+ \
                     riutils.seq2list(self, nverts)+' '+riutils.seq2list(self, vertids)+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")


    # Predefined basis matrices
    RiHermiteBasis = "hermite"
    RiCatmullRomBasis = "catmull-rom"
    RiBezierBasis = "bezier"
    RiBSplineBasis = "b-spline"
    RiPowerBasis = "power"

    # RiBasis
    def RiBasis(self, ubasis, ustep, vbasis, vstep):
        """Set the current basis for the u and v direction.

        ubasis/vbasis can either be one of the predefined basis matrices
        RiHermiteBasis, RiCatmullRomBasis, RiBezierBasis, RiBSplineBasis,
        RiPowerBasis or it can be a user defined matrix.

        For the predefined matrices there are also predefined variables
        which can be used for the step parameters:
        RI_HERMITESTEP, RI_CATMULLROMSTEP, RI_BEZIERSTEP, RI_BSPLINESTEP,
        RI_POWERSTEP.

        Example: RiBasis(RiBezierBasis, RI_BEZIERSTEP,
                         RiHermiteBasis, RI_HERMITESTEP)
        """

        if type(ubasis)==types.StringType:
            ubasis = '"'+ubasis+'"'
        else:
            ubasis = riutils.seq2list(self, ubasis, 16)
            
        if type(vbasis)==types.StringType:
            vbasis = '"'+vbasis+'"'
        else:
            vbasis = riutils.seq2list(self, vbasis, 16)
            
        self._ribout.write('Basis '+ubasis+' '+str(ustep)+' '+vbasis+' '+str(vstep)+"\n")

    # RiPatch
    def RiPatch(self, type, *paramlist, **keyparams):
        """RiPatch(type, paramlist)

        type is one of RI_BILINEAR (4 vertices) or RI_BICUBIC (16 vertices).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: 4
        uniform:  1              vertex:  4/16 (depends on type)

        Example: RiPatch(RI_BILINEAR, P=[0,0,0, 1,0,0, 0,1,0, 1,1,0])
        """

        self._ribout.write('Patch "'+type+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiPatchMesh
    def RiPatchMesh(self, type, nu, uwrap, nv, vwrap, *paramlist, **keyparams):
        """Create a mesh made of patches.

        type is one of RI_BILINEAR or RI_BICUBIC.
        uwrap/vwrap can be RI_PERIODIC or RI_NONPERIODIC.
        The number of control points is nu*nv.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #patch corners (depends on uwrap/vwrap)
        uniform:  #patches       vertex:  nu*nv (same as "P")

        """

        self._ribout.write('PatchMesh "'+type+'" '+str(nu)+' "'+uwrap+'" '+\
                     str(nv)+' "'+vwrap+'"'+\
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")
        

    # RiNuPatch
    def RiNuPatch(self, nu, uorder, uknot, umin, umax, nv, vorder, vknot, vmin, vmax, *paramlist, **keyparams):
        """Create a NURBS patch.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #segment corners
        uniform:  #segments      vertex:  nu*nv
        """

        self._ribout.write('NuPatch '+str(nu)+" "+str(uorder)+' '+riutils.seq2list(self, uknot)+" "+ \
                     str(umin)+" "+str(umax)+" "+ \
                    str(nv)+" "+str(vorder)+' '+riutils.seq2list(self, vknot)+" "+ \
                     str(vmin)+" "+str(vmax)+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiTrimCurve
    def RiTrimCurve(self, ncurves, order, knot, min, max, n, u, v, w):
        """Set the current trim curve.
        """

        self._ribout.write('TrimCurve '+riutils.seq2list(self, ncurves)+' '+\
                     riutils.seq2list(self, order)+' '+riutils.seq2list(self, knot)+' '+\
                     riutils.seq2list(self, min)+' '+riutils.seq2list(self, max)+' '+riutils.seq2list(self, n)+' '+ \
                     riutils.seq2list(self, u)+' '+ \
                     riutils.seq2list(self, v)+' '+ \
                     riutils.seq2list(self, w)+'\n')

    # RiPoints
    def RiPoints(self, *paramlist, **keyparams):
        """Create individual points.

        The size of the points can be either set with the primitive variable
        RI_WIDTH (one float per point) or RI_CONSTANTWIDTH (one float for all
        points).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #points
        uniform:  1              vertex:  #points    
        """

        self._ribout.write('Points'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiCurves
    def RiCurves(self, type, nvertices, wrap, *paramlist, **keyparams):
        """Create a number of curve primitives.

        type is either RI_LINEAR or RI_CUBIC.
        nvertices is an array with the number of vertices in each curve.
        wrap is either RI_PERIODIC or RI_NONPERIODIC.
        The width of the curves can be specified with the parameter
        RI_WIDTH (varying float) or RI_CONSTANTWIDTH (constant float).

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #segments (depends on type and wrap)
        uniform:  #curves        vertex:  #points

        Example: RiCurves(RI_CUBIC, [4], RI_NONPERIODIC,
                          P=[0,0,0, -1,-0.5,1, 2,0.5,1, 1,0,-1],
                          width=[0.1, 0.04])
        """

        self._ribout.write('Curves "'+type+'" '+riutils.seq2list(self, nvertices)+' "'+wrap+'"'+
                      riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiSubdivisionMesh
    def RiSubdivisionMesh(self, scheme, nverts, vertids, tags, nargs, intargs, floatargs, *paramlist, **keyparams):
        """Create a subdivision surface.

        The only standard scheme is currently "catmull-clark".
        nverts:  The number of vertices in each face
        vertids: The vertex indices of the face vertices (0-based)
        tags: A string array of tag names.
        nargs: The number of int and float args for each tag.
        intargs: The integer arguments.
        floatargs: The float arguments.
        The vertices themselves are stored in the parameter list (parameter "P").
        

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: #vertices (*)
        uniform:  #faces         vertex:  #vertices (*)

        (*) max(vertids)+1
        """

        if len(tags)==0:
            self._ribout.write('SubdivisionMesh "'+scheme+'" '+riutils.seq2list(self, nverts)+' '+ \
                     riutils.seq2list(self, vertids)+' '+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")
        else:
            self._ribout.write('SubdivisionMesh "'+scheme+'" '+riutils.seq2list(self, nverts)+' '+ \
                     riutils.seq2list(self, vertids)+' '+riutils.seq2list(self, tags)+' '+ \
                     riutils.seq2list(self, nargs)+' '+riutils.seq2list(self, intargs)+' '+ \
                     riutils.seq2list(self, floatargs)+' '+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiBlobby
    def RiBlobby(self, nleaf, code, floats, strings, *paramlist, **keyparams):
        """Create a blobby surface.

        Number of array elements for primitive variables:
        -------------------------------------------------
        constant: 1              varying: nleaf
        uniform:  1              vertex:  nleaf

        Example: RiBlobby(2, [1001,0, 1003,0,16, 0,2,0,1],
                          [1.5,0,0,0, 0,1.5,0,0, 0,0,1.5,0, 0,0,-.1,1,
                          0.4, 0.01,0.3, 0.08], ["flat.zfile"])
        """

        self._ribout.write('Blobby '+str(nleaf)+' '+riutils.seq2list(self, code)+' '+riutils.seq2list(self, floats)+
                      ' '+riutils.seq2list(self, strings)+
                      riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiColorSamples
    def RiColorSamples(self, nRGB, RGBn):
        """Redefine the number of color components to be used for specifying colors.

        nRGB is a n x 3 matrix that can be used to transform the n component color
        to a RGB color (n -> RGB).
        RGBn is just the opposite, its a 3 x n matrix that's used to transform
        a RGB color to a n component color (RGB -> n).
        Thus, the new number of color components is len(matrix)/3 (matrix is
        either nRGB or RGBn).

        Example: RiColorSamples([0.3,0.3,0.3], [1,1,1])
        """

        if len(nRGB)!=len(RGBn):
            self._error(RIE_CONSISTENCY, RIE_ERROR,
                   "The color transformation matrices must have the same number of values.")

        if len(nRGB)%3!=0 or len(nRGB)==0:
            self._error(RIE_CONSISTENCY, RIE_ERROR,
                   "The number of values in the transformation matrices must be a multiple of 3.")
            
        self._colorsamples = len(riutils.flatten(nRGB))/3
        self._ribout.write('ColorSamples '+riutils.seq2list(self, nRGB)+' '+riutils.seq2list(self, RGBn)+'\n')

    # RiColor
    def RiColor(self, Cs):
        """Set the current color.

        Cs must be a sequence of at least N values where N is the number of
        color samples (set by RiColorSamples(), default is 3).

        Example: RiColor([0.2,0.5,0.2])
        """

        col=riutils.seq2col(self, Cs)
        self._ribout.write("Color "+col+"\n")

    # RiOpacity
    def RiOpacity(self, Os):
        """Set the current opacity.

        Os must be a sequence of at least N values where N is the number
        of color samples (set by RiColorSamples(), default is 3). The
        opacity values must lie in the range from 0 to 1 (where 0 means
        completely transparent and 1 means completely opaque).

        Example: RiOpacity([0,0,1])
        """

        col=riutils.seq2col(Os)
        self._ribout.write("Opacity "+col+"\n")

    # RiShadingRate
    def RiShadingRate(self, size):
        """Set the current shading rate to an area of size pixels.

        Example: RiShadingRate(1.0)
        """

        self._ribout.write("ShadingRate %s\n"%size)

    # RiShadingInterpolation
    def RiShadingInterpolation(self, type):
        """Specify how shading samples are interpolated.

        type can be RI_CONSTANT or RI_SMOOTH.

        Example: RiShadingInterpolation(RI_SMOOTH)"""

        self._ribout.write('ShadingInterpolation "'+type+'"\n')

    # RiShader
    def RiShader(self, name, handle, *paramlist, **keyparams):
        """Set the current coshader.

        Example: RiShader("plastic", "plastic_layer", Kd=0.7, Ks=0.3)"""

        self._ribout.write('Shader "'+name+'"'+' "'+handle+'"'+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")
        
    # RiSurface
    def RiSurface(self, name, *paramlist, **keyparams):
        """Set the current surface shader.

        Example: RiSurface("plastic", Kd=0.7, Ks=0.3)"""

        self._ribout.write('Surface "'+name+'"'+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiInterior
    def RiInterior(self, name, *paramlist, **keyparams):
        """Set the current interior volume shader.

        Example: RiInterior("water")
        """

        self._ribout.write('Interior "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiExterior
    def RiExterior(self, name, *paramlist, **keyparams):
        """Set the current exterior volume shader.

        Example: RiExterior("fog")
        """

        self._ribout.write('Exterior "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiAtmosphere
    def RiAtmosphere(self, name, *paramlist, **keyparams):
        """Set the current atmosphere shader.

        If name is RI_NULL then no atmosphere shader is used.

        Example: RiAtmosphere("fog")
        """

        if name==RI_NULL:
            self._ribout.write('Atmosphere\n')
        else:
            self._ribout.write('Atmosphere "'+name+'"'+ \
                          riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiDisplacement
    def RiDisplacement(self, name, *paramlist, **keyparams):
        """Set the current displacement shader.

        Example: RiDisplacement("dented", km=1.5)
        """

        self._ribout.write('Displacement "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiImager
    def RiImager(self, name, *paramlist, **keyparams):
        """Set an imager shader.

        if name is RI_NULL, no imager shader is used.

        Example: RiImager("background", "color bgcolor", [0.3,0.3,0.9])
        """

        if name==RI_NULL:
            self._ribout.write('Imager\n')
        else:
            self._ribout.write('Imager "'+name+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiClipping
    def RiClipping(self, near, far):
        """Sets the near and the far clipping plane along the direction of view.

        near and far must be positive values in the range from RI_EPSILON to
        RI_INFINITY.

        Example: RiClipping(0.1, 100)
        """

        self._ribout.write("Clipping %s %s\n"%(near,far))

    # RiClippingPlane
    def RiClippingPlane(self, x, y, z, nx, ny, nz):
        """Adds a new clipping plane, defined by a surface point and its normal.

        All the geometry in positive normal direction is clipped.

        Example: RiClippingPlane(0,0,0, 0,0,-1) clips everything below the XY plane
        """

        self._ribout.write('ClippingPlane %s %s %s %s %s %s\n'%(x,y,z,nx,ny,nz))

    # RiDisplay
    def RiDisplay(self, name,type,mode, *paramlist, **keyparams):
        """Specify the destination and type of the output.

        Example: RiDisplay("frame0001.tif", RI_FILE, RI_RGB)
                 RiDisplay("myimage.tif", RI_FRAMEBUFFER, RI_RGB)
        """

        self._ribout.write('Display "'+name+'" "'+type+'" "'+mode+'"'+ \
                     riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiDisplayChannel
    def RiDisplayChannel(self, channel, *paramlist, **keyparams):
        """Defines a new display channel.

        Example: RiDisplayChannel("color aovCi", "string opacity", "aovOi")
        """
        self._ribout.write('DisplayChannel "%s"%s\n'%(channel, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiFormat
    def RiFormat(self, xres, yres, aspect):
        """Set the resolution of the output image and the aspect ratio of a pixel.

        Example: RiFormat(720,576,1)"""

        self._ribout.write('Format %s %s %s\n'%(xres, yres, aspect))

    # RiFrameAspectRatio
    def RiFrameAspectRatio(self, frameratio):
        """Set the ratio between width and height of the image.

        Example: RiFrameAspectRatio(4.0/3)
        """

        self._ribout.write('FrameAspectRatio %s\n'%frameratio)

    # RiGeometricApproximation
    def RiGeometricApproximation(self, type, value):
        """Sets parameters for approximating surfaces.

        Example: RiGeometricApproximation(RI_FLATNESS, 0.5)  (default value)
        """

        self._ribout.write('GeometricApproximation "'+type+'" '+str(value)+"\n")


    # RiProjection
    def RiProjection(self, name, *paramlist, **keyparams):
        """Specify a projection method.

        The standard projections are RI_PERSPECTIVE and RI_ORTHOGRAPHIC.
        The perspective projection takes one optional parameter, RI_FOV.

        Example: RiProjection(RI_PERSPECTIVE, fov=45)
        """

        if name==RI_NULL:
            self._ribout.write('Projection\n')
        else:
            self._ribout.write('Projection "'+name+'"'+ \
                          riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiCamera
    def RiCamera(self, name, *paramlist, **keyparams):
        """Mark the current camera description.

        Example: RiCamera("rightcamera")
        """
        self._ribout.write('Camera "%s"%s\n'%(name, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiScreenWindow
    def RiScreenWindow(self, left, right, bottom, top):
        """Specify the extents of the output image on the image plane.

        Example: RiScreenWindow(-1,1,-1,1)
        """

        self._ribout.write('ScreenWindow %s %s %s %s\n'%(left, right, bottom, top))

    # RiCropWindow
    def RiCropWindow(self, left, right, bottom, top):
        """Specify a subwindow to render.

        The values each lie between 0 and 1.

        Example: RiCropWindow(0.0, 1.0 , 0.0, 1.0)  (renders the entire frame)
                 RiCropWindow(0.5, 1.0 , 0.0, 0.5)  (renders the top right quarter)
        """

        self._ribout.write('CropWindow %s %s %s %s\n'%(left, right, bottom, top))

    # RiPixelSamples
    def RiPixelSamples(self, xsamples, ysamples):
        """Set the sampling rate in horizontal and vertical direction.

        Example: RiPixelSamples(2,2)"""

        self._ribout.write("PixelSamples %s %s\n"%(max(1,xsamples), max(1,ysamples)))

    # RiPixelVariance
    def RiPixelVariance(self, variance):
        """Limit the acceptable variance in the output value of pixels.

        Example: RiPixelVariance(0.01)"""

        self._ribout.write('PixelVariance %s\n'%variance)

    # Predefined filter functions:
    RiGaussianFilter   = "gaussian"
    RiBoxFilter        = "box"
    RiTriangleFilter   = "triangle"
    RiSincFilter       = "sinc"
    RiCatmullRomFilter = "catmull-rom"

    # RiPixelFilter
    def RiPixelFilter(self, function, xwidth, ywidth):
        """Set a pixel filter function and its width in pixels.

        Note: Here you can only use one of the predefined filter functions:
        RiGaussianFilter, RiBoxFilter, RiTriangleFilter, RiSincFilter and
        RiCatmullRomFilter.
        Passing a callable as filter function will issue a warning and ignore
        the call.

        Example: RiPixelFilter(RiGaussianFilter, 2.0, 1.0)"""
        
        if callable(function):
            self._error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
            return

        self._ribout.write('PixelFilter "'+function+'" '+str(xwidth)+' '+str(ywidth)+'\n')

    # RiExposure
    def RiExposure(self, gain, gamma):
        """Sets the parameters for the output color transformation.

        The transformation is color_out = (color_in*gain)^(1/gamma)

        Example: RiExposure(1.3, 2.2)
        """

        self._ribout.write("Exposure %s %s\n"%(gain, gamma))

    # RiQuantize
    def RiQuantize(self, type, one, min, max, ditheramplitude):
        """Set the quantization parameters for colors and depth.

        Example: RiQuantize(RI_RGBA, 2048, -1024, 3071, 1.0)
        """

        self._ribout.write('Quantize "%s" %s %s %s %s\n'%(type, one, min, max, ditheramplitude))
        

    # RiDepthOfField
    def RiDepthOfField(self, fstop, focallength, focaldistance):
        """Set depth of field parameters.

        If fstop is RI_INFINITY depth of field is turned off.

        Example: RiDepthOfField(22,45,1200)
        """

        if fstop==RI_INFINITY:
            self._ribout.write('DepthOfField\n')
        else:
            self._ribout.write('DepthOfField %s %s %s\n'%(fstop, focallength, focaldistance))

    # RiMotionBegin
    def RiMotionBegin(self, *times):
        """Start the definition of a moving primitive.

        You can specify the time values directly or inside a sequence,
        for example, RiMotionBegin(0,1) or RiMotionBegin([0,1]).

        Example: RiMotionBegin(0.0, 1.0)
                 RiTranslate(1.0, 0.0, 0.0)
                 RiTranslate(1.0, 2.0, 0.0)
                 RiMotionEnd()
        """


        if self._insidemotion:
            self._error(RIE_ILLSTATE, RIE_ERROR, "Motion blocks cannot be nested.")

        self._ribout.write('MotionBegin '+riutils.seq2list(self, times)+'\n')
        self._insidemotion = 1

    # RiMotionEnd
    def RiMotionEnd(self):
        "Terminates the definition of a moving primitive."


        self._ribout.write('MotionEnd\n')
        self._insidemotion = 0

    # RiShutter
    def RiShutter(self, opentime, closetime):
        """Set the times at which the shutter opens and closes.

        Example: RiShutter(0.1, 0.9)
        """

        self._ribout.write('Shutter %s %s\n'%(opentime, closetime))

    # RiTranslate
    def RiTranslate(self, *translation):
        """Concatenate a translation onto the current transformation.

        The translation is either given as 3 scalars or a sequence of
        3 scalars.

        Example: RiTranslate(1.2, 4.3, -0.5)
                 or
                 RiTranslate( (1.2, 4.3, -0.5) )
        """

        # Argument = sequence?
        if len(translation)==1:
            s=riutils.seq2list(self, translation,3)
            self._ribout.write('Translate '+s[1:-1]+"\n")
        # Argument = 3 scalars?
        elif len(translation)==3:
            dx,dy,dz=translation
            self._ribout.write('Translate %s %s %s\n'%(dx,dy,dz))
        # Invalid argument size
        else:
            raise TypeError, "RiTranslate() only takes a sequence or three scalars as arguments"

    # RiRotate
    def RiRotate(self, angle, *axis):
        """Rotate about angle degrees about the given axis.

        The axis is either given as 3 scalars or a sequence of 3 scalars.

        Example: RiRotate(90, 1,0,0)
        """

        # Argument = sequence?
        if len(axis)==1:
            s=riutils.seq2list(self, axis,3)
            self._ribout.write('Rotate %s %s\n'%(angle, s[1:-1]))
        # Argument = 3 scalars?
        elif len(axis)==3:
            ax,ay,az=axis
            self._ribout.write('Rotate %s %s %s %s\n'%(angle, ax, ay, az))
        # Invalid argument size
        else:
            raise TypeError, "RiRotate() only takes 2 or 4 arguments ("+`len(axis)+1`+" given)"


    # RiScale
    def RiScale(self, *scaling):
        """Concatenate a scaling onto the current transformation.

        The scaling is either given as 3 scalars or a sequence of 3 scalars.

        Example: RiScale(2,2,2)"""

        # Argument = sequence?
        if len(scaling)==1:
            s=riutils.seq2list(self, scaling,3)
            self._ribout.write('Scale '+s[1:-1]+"\n")
        # Argument = 3 scalars?
        elif len(scaling)==3:
            sx,sy,sz=scaling
            self._ribout.write('Scale %s %s %s\n'%(sx, sy, sz))
        # Invalid argument size
        else:
            raise TypeError, "RiScale() only takes a sequence or three scalars as arguments"


    # RiSkew
    def RiSkew(self, angle, *vecs):
        """Concatenate a skew onto the current transformation.

        angle is given in degrees.
        The two vectors are each given as 3 scalars or a sequence
        of 3 scalars.

        Example: RiSkew(45, 0,1,0, 1,0,0)
        """

        # Argument = two sequences?
        if len(vecs)==2:
            s1=riutils.seq2list(self, vecs[0],3)
            s2=riutils.seq2list(self, vecs[1],3)
            self._ribout.write('Skew '+str(angle)+" "+s1[1:-1]+" "+s2[1:-1]+"\n")
        # Argument = 6 scalars?
        elif len(vecs)==6:
            dx1,dy1,dz1,dx2,dy2,dz2=vecs
            self._ribout.write('Skew %s %s %s %s %s %s %s\n'%(angle, dx1, dy1, dz1, dx2, dy2, dz2))
        # Invalid argument size
        else:
            raise TypeError, "RiSkew() only takes 3 or 7 arguments ("+`len(vecs)+1`+" given)"


    # RiPerspective
    def RiPerspective(self, fov):
        """Concatenate a perspective transformation onto the current transformation.
        
        Example: RiPerspective(45)"""

        self._ribout.write('Perspective %s\n'%fov)

    # RiIdentity
    def RiIdentity(self):
        """Set the current transformation to the identity.

        Example: RiIdentity()
        """

        self._ribout.write('Identity\n')

    # RiConcatTransform
    def RiConcatTransform(self, transform):
        """Concatenate a transformation onto the current transformation.

        transform must be a sequence that evaluates to 16 floating point
        values (4x4 matrix).

        Example: RiConcatTransform([2,0,0,0, 0,2,0,0, 0,0,2,0, 0,0,0,1])
                 RiConcatTransform([[2,0,0,0], [0,2,0,0], [0,0,2,0], [0,0,0,1]])
        """

        self._ribout.write('ConcatTransform '+riutils.seq2list(self, transform,16)+"\n")

    # RiTransform
    def RiTransform(self, transform):
        """Set the current transformation.

        transform must be a sequence that evaluates to 16 floating point
        values (4x4 matrix).

        Example: RiTransform([2,0,0,0, 0,2,0,0, 0,0,2,0, 0,0,0,1])
                 RiTransform([[2,0,0,0], [0,2,0,0], [0,0,2,0], [0,0,0,1]])
        """

        self._ribout.write('Transform '+riutils.seq2list(self, transform,16)+"\n")

    # RiSides
    def RiSides(self, nsides):
        """Specify the number of visible sides of subsequent surfaces.

        Example: RiSides(1)"""

        if nsides!=1 and nsides!=2:
            self._error(RIE_RANGE, RIE_ERROR, "The number of sides (nsides) must be either 1 or 2.")

        self._ribout.write('Sides %s\n'%nsides)

    # RiOrientation
    def RiOrientation(self, orientation):
        """Set the orientation of subsequent surfaces.

        orientation is either RI_OUTSIDE, RI_INSIDE, RI_LH (left handed)
        or RI_RH (right handed).
        """

        self._ribout.write('Orientation "'+orientation+'"\n')

    # RiReverseOrientation
    def RiReverseOrientation(self):
        """Causes the current orientation to be toggled.

        Example: RiReverseOrientation()
        """

        self._ribout.write('ReverseOrientation\n')

    # RiMatte
    def RiMatte(self, onoff):
        """Indicates whether subsequent primitives are matte objects.

        Example: RiMatte(RI_TRUE)
        """
        if onoff:
            self._ribout.write('Matte 1\n')
        else:
            self._ribout.write('Matte 0\n')

    # RiLightSource
    def RiLightSource(self, name, *paramlist, **keyparams):
        """Add another light source and return its light handle.

        name is the name of the light source shader. You can set a user defined
        string handle via the RI_HANDLEID parameter.

        Example: light1 = RiLightSource("distantlight", intensity=1.5)
        """

        paramlist = riutils.merge_paramlist(paramlist, keyparams)
        lshandle = None
        for i in range(0, len(paramlist), 2):
            token = paramlist[i]
            if token==RI_HANDLEID:
                lshandle = str(paramlist[i+1])
                paramlist = paramlist[:i]+paramlist[i+2:]
                break

        # Check if the user provided a handle id...
        if lshandle is None:
            self._lighthandle += 1
            lshandle = self._lighthandle
            self._ribout.write('LightSource "%s" %d%s\n'%(name, lshandle, riutils.paramlist2string(self, paramlist, {})))
        else:
            self._ribout.write('LightSource "%s" "%s"%s\n'%(name, lshandle, riutils.paramlist2string(self, paramlist, {})))
            
        return lshandle

    # RiIlluminate
    def RiIlluminate(self, light, onoff):
        """Activate or deactive a light source.

        Example: RiIlluminate(lgt, RI_TRUE)
        """

        if type(light)==str or type(light)==unicode:
            self._ribout.write('Illuminate "%s" %d\n'%(light, onoff))
        else:
            self._ribout.write('Illuminate %d %d\n'%(light, onoff))
            

    # RiAreaLightSource
    def RiAreaLightSource(self, name, *paramlist, **keyparams):
        """Start the definition of an area light and return the light handle.

        You can set a user defined string handle via the RI_HANDLEID parameter.
        
        Example: RiAttributeBegin()
                 area1 = RiAreaLightSource("arealight", intensity=0.75)
                 ....
                 RiAttributeEnd()
                 RiIlluminate(area1, RI_TRUE)
        """

        # Check if the user provided a handle id...
        if RI_HANDLEID in keyparams:
            lshandle = str(keyparams[RI_HANDLEID])
            del keyparams[RI_HANDLEID]
            self._ribout.write('AreaLightSource "%s" "%s"%s\n'%(name, lshandle, riutils.paramlist2string(self, (), keyparams)))
        else:
            self._lighthandle+=1
            lshandle = self._lighthandle
            self._ribout.write('AreaLightSource "%s" %d%s\n'%(name, lshandle, riutils.paramlist2string(self, (), keyparams)))

        return lshandle

    # RiDeclare
    def RiDeclare(self, name, declaration):
        """Declare the name and type of a variable.

        The syntax of the declaration is:  [class] [type] ['['n']']

        class ::= constant | uniform | varying | vertex
        type  ::= float | integer | string | color | point | vector | normal |
                  matrix | hpoint
        
        Example: RiDeclare("foo","uniform float")
                 RiDeclare("bar","constant integer [4]")
                 RiDeclare("mycolor", "varying color")
        """

        if declaration==RI_NULL:
            declaration=""
            
        self._ribout.write('Declare "'+name+'" "'+declaration+'"\n')
        self._declarations[name]=declaration
        return name

    # RiArchiveRecord
    def RiArchiveRecord(self, type, format, *args):
        """Output a user data record.

        type is one of RI_COMMENT, RI_STRUCTURE or RI_VERBATIM.

        For comments and structural hints you can use the special variables
        $CREATOR, $DATE and $USER which will be replaced by their appropriate
        value (program name, date string, user name).

        Example: RiArchiveRecord(RI_COMMENT, "Frame %d", 2)
                 RiArchiveRecord(RI_STRUCTURE, "CreationDate $DATE")
        """

        if type!=RI_VERBATIM and format.find("$")!=-1:
            format = format.replace("$DATE", time.ctime())
            format = format.replace("$CREATOR", sys.argv[0])
            try:
                user = getpass.getuser()
            except:
                user = "<unknown>"
            format = format.replace("$USER", user)

        if type==RI_COMMENT:
            outstr = "# "+format%args+"\n"
        elif type==RI_STRUCTURE:
            outstr = "##"+format%args+"\n"
        elif type==RI_VERBATIM:
            outstr = format%args
        else:
            return

        # Use the writeArchiveRecord() if there is any, otherwise use write()
        # (the latter case happens when RiBegin() wasn't called. self._ribout is
        # then set to stdout)
        if hasattr(self._ribout, "writeArchiveRecord"):
            self._ribout.writeArchiveRecord(outstr)
        else:
            self._ribout.write(outstr)
        
        
    # RiReadArchive
    def RiReadArchive(self, filename, callback=None, *ignore):
        """Include an archive file.

        In this implementation the callback function is not used and can
        be left out.

        Example: RiReadArchive("teapot.rib")"""

        self._ribout.write('ReadArchive "'+filename+'"\n')

    # RiArchiveBegin
    def RiArchiveBegin(self, archivename, *paramlist, **keyparams):
        """Begin an inline archive.
        
        Example: RiArchiveBegin("myarchive")
                 ...
                 RiArchiveEnd()
                 RiReadArchive("myarchive")
        """
        self._ribout.write('ArchiveBegin "%s"%s\n'%(archivename, riutils.paramlist2string(self, (), keyparams)))
        return archivename

    # RiArchiveEnd
    def RiArchiveEnd(self):
        """Terminate an inline archive.
        
        Example: RiArchiveBegin("myarchive")
                 ...
                 RiArchiveEnd()
                 RiReadArchive("myarchive")
        """
        self._ribout.write('ArchiveEnd\n')


    def RiProcDelayedReadArchive(self): return "DelayedReadArchive"
    def RiProcRunProgram(self): return "RunProgram"
    def RiProcDynamicLoad(self): return "DynamicLoad"
    def RiProcFree(self, data): pass

    # RiProcedural
    def RiProcedural(self, data, bound, subdividefunc, freefunc=None):
        """Declare a procedural model.

        subdividefunc and freefunc may either be the standard RenderMan
        procedurals (RiProcDelayedReadArchive, RiProcRunProgram,
        RiProcDynamicLoad and RiProcFree) or Python callables.
        In the former case, data must be a sequence of strings or a single
        string containing the data for the functions. In the latter case,
        data may be any Python object which is just passed on to the
        functions. 
        freefunc is optional and defaults to None.

        Because this module can only produce RIB, a custom subdivide function is
        simply called with a detail value of RI_INFINITY to generate all the
        data at once.
        
        Example: RiProcedural("mymodel.rib", [-1,1,-1,1,-1,1], \\
                              RiProcDelayedReadArchive, RI_NULL)
                              
                 RiProcedural(["python teapot.py",""],[0,1,0,1,0,1], \\
                              RiProcRunProgram, RI_NULL)
                              
                 RiProcedural(["teapot.so",""],[0,1,0,1,0,1], \\
                              RiProcDynamicLoad, RI_NULL)
        """
        if subdividefunc in [RiProcDelayedReadArchive, RiProcRunProgram, RiProcDynamicLoad]:
            if type(data)==types.StringType:
                data=[data]
            self._ribout.write('Procedural "'+subdividefunc()+'" '+riutils.seq2list(self, data)+ \
                         ' '+riutils.seq2list(self, bound,6)+"\n")
        else:
            # Call the custom procedure to generate all the data...
            subdividefunc(data, RI_INFINITY)
            if freefunc is not None:
                freefunc(data)

    # RiGeometry
    def RiGeometry(self, type, *paramlist, **keyparams):
        """Create an implementation-specific geometric primitive.

        Example: RiGeometry("teapot")
        """

        self._ribout.write('Geometry "'+type+'"'+riutils.paramlist2string(self, paramlist, keyparams)+"\n")

    # RiBound
    def RiBound(self, bound):
        """Set the bounding box for subsequent primitives.

        bound must be a sequence of six floating point values specifying
        the extent of the box along each coordinate direction:
        bound = [xmin, xmax, ymin, ymax, zmin, zmax]

        Example: RiBound([-1,1, 0,1, 0.5,0.75])
        """

        self._ribout.write('Bound '+riutils.seq2list(self, bound,6)+'\n')
        
    # RiSolidBegin
    def RiSolidBegin(self, type):
        """Start the definition of a solid object.

        type is one of RI_PRIMITIVE, RI_UNION, RI_DIFFERENCE and RI_INTERSECTION.

        Example: RiSolidBegin(RI_INTERSECTION)
                 RiSolidBegin(RI_PRIMITIVE)
                 ...
                 RiSolidEnd()
                 RiSolidBegin(RI_PRIMITIVE)
                 ...
                 RiSolidEnd()
                 RiSolidEnd()
        """

        self._ribout.write('SolidBegin "'+type+'"\n')

    # RiSolidEnd
    def RiSolidEnd(self):
        """Terminate the definition of a solid object."""

        self._ribout.write('SolidEnd\n')

    # RiObjectBegin
    def RiObjectBegin(self, *paramlist, **keyparams):
        """Start the definition of a retained model and return the object handle.

        You can pass a user defined string handle via the RI_HANDLEID parameter.

        Example: obj1 = RiObjectBegin()
                 ...
                 RiObjectEnd()
        """

        if self._insideobject:
            self._error(RIE_ILLSTATE, RIE_ERROR, "Object blocks cannot be nested.")

        keyparams = riutils.paramlist2dict(self, paramlist, keyparams)

        # Check if the user provided a handle id...
        if RI_HANDLEID in keyparams:
            objhandle = keyparams[RI_HANDLEID]
            del keyparams[RI_HANDLEID]
            if isinstance(objhandle, int):
                self._ribout.write('ObjectBegin %d\n'%objhandle)
            else:
                self._ribout.write('ObjectBegin "%s"\n'%str(objhandle))
        else:
            self._objecthandle+=1
            objhandle = self._objecthandle
            self._ribout.write('ObjectBegin %d\n'%objhandle)
        
        self._insideobject=1

        return objhandle

    # RiObjectEct
    def RiObjectEnd(self):
        """Terminate the definition of a retained model."""

        self._ribout.write('ObjectEnd\n')
        self._insideobject=0

    # RiObjectInstance
    def RiObjectInstance(self, handle):
        """Create an instance of a previously defined model.

        Example: RiObjectInstance(obj1)
        """

        if type(handle)==str or type(handle)==unicode:
            self._ribout.write('ObjectInstance "%s"\n'%handle)
        else:
            self._ribout.write('ObjectInstance %d\n'%handle)

    # RiTextureCoordinates
    def RiTextureCoordinates(self, s1, t1, s2, t2, s3, t3, s4, t4):
        """Set the current set of texture coordinates.

        Declares a projection from the unit square [(0,0), (1,0), (0,1), (1,1)]
        in parameter space to quadrilateral [(s1,t1), (s2,t2), (s3,t3), (s4,t4)]
        in texture space.

        Example: RiTextureCoordinates(0.0, 0.0, 2.0, -0.5, -0.5, 1.75, 3.0, 3.0)"""

        self._ribout.write('TextureCoordinates %s %s %s %s %s %s %s %s\n'%(s1,t1,s2,t2,s3,t3,s4,t4))

    # RiMakeTexture
    def RiMakeTexture(self, picname, texname, swrap, twrap, filterfunc, swidth, twidth, *paramlist, **keyparams):
        """Convert an image file into a texture file.

        swrap and twrap are one of RI_PERIODIC, RI_CLAMP or RI_BLACK.
        filterfunc has to be one of the predefined filter functions:
        RiGaussianFilter, RiBoxFilter, RiTriangleFilter, RiSincFilter or
        RiCatmullRomFilter (otherwise a warning is issued and the call is ignored).
        swidth and twidth define the support of the filter.

        Example: RiMakeTexture("img.tif", "tex.tif", RI_PERIODIC, RI_CLAMP, \\
                               RiGaussianFilter, 2,2)
        """
        
        if callable(filterfunc):
            self._error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
            return

        self._ribout.write('MakeTexture "'+picname+'" "'+texname+'" "'+swrap+'" "'+
                      twrap+'" "'+filterfunc+'" '+str(swidth)+' '+str(twidth)+
                      riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiMakeLatLongEnvironment
    def RiMakeLatLongEnvironment(self, picname, texname, filterfunc, swidth, twidth, *paramlist, **keyparams):
        """Convert an image file into an environment map.

        filterfunc has to be one of the predefined filter functions:
        RiGaussianFilter, RiBoxFilter, RiTriangleFilter, RiSincFilter or
        RiCatmullRomFilter (otherwise a warning is issued and the call is ignored).
        swidth and twidth define the support of the filter.

        Example: RiMakeLatLongEnvironment("img.tif", "tex.tif",
                                          RiGaussianFilter, 2,2)
        """
        
        if callable(filterfunc):
            self._error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
            return

        self._ribout.write('MakeLatLongEnvironment "'+picname+'" "'+texname+'" "'+
                      filterfunc+'" '+str(swidth)+' '+str(twidth)+
                      riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiMakeCubeFaceEnvironment
    def RiMakeCubeFaceEnvironment(self, px,nx,py,ny,pz,nz, texname, fov, filterfunc, swidth, twidth, *paramlist, **keyparams):
        """Convert six image files into an environment map.

        The px/nx images are the views in positive/negative x direction.
        fov is the field of view that was used to generate the individual images.
        filterfunc has to be one of the predefined filter functions:
        RiGaussianFilter, RiBoxFilter, RiTriangleFilter, RiSincFilter or
        RiCatmullRomFilter (otherwise a warning is issued and the call is ignored).
        swidth and twidth define the support of the filter.

        Example: RiMakeCubeFaceEnvironment("px.tif","nx.tif","py.tif","ny.tif",
                                           "pz.tif","nz.tif", "tex.tif", 92.0,
                                            RiGaussianFilter, 2,2)
        """
        
        if callable(filterfunc):
            self._error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
            return

        self._ribout.write('MakeCubeFaceEnvironment "'+px+'" "'+nx+'" "'+
                      py+'" "'+ny+'" "'+pz+'" "'+nz+'" "'+ texname+'" '+
                      str(fov)+' "'+filterfunc+'" '+str(swidth)+' '+str(twidth)+
                      riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiMakeShadow
    def RiMakeShadow(self, picname, shadowname, *paramlist, **keyparams):
        """Transform a depth image into a shadow map.

        Example: RiMakeShadow("depthimg.tif", "shadow.tif")
        """
        
        self._ribout.write('MakeShadow "'+picname+'" "'+shadowname+'"'+riutils.paramlist2string(self, paramlist, keyparams)+'\n')

    # RiMakeBrickMap
    def RiMakeBrickMap(self, ptcnames, bkmname, *paramlist, **keyparams):
        """Create a brick map file from a list of point cloud file names.

        Example: RiMakeBrickMap(["sphere.ptc", "box.ptc"], "spherebox.bkm", "float maxerror", 0.002)
        """
        names = " ".join(map(lambda name: '"%s"'%name, ptcnames))
        self._ribout.write('MakeBrickMap [%s] "%s"%s\n'%(names, bkmname, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiDetail
    def RiDetail(self, bound):
        """Set the current bounding box.

        bound must be a sequence of six floating point values specifying
        the extent of the box along each coordinate direction:
        bound = [xmin, xmax, ymin, ymax, zmin, zmax]

        Example: RiDetail([10,20,40,70,0,1])
        """

        self._ribout.write('Detail '+riutils.seq2list(self, bound,6)+'\n')

    # RiRelativeDetail
    def RiRelativeDetail(self, relativedetail):
        """Set the factor for all level of detail calculations.

        Example: RiRelativeDetail(0.7)"""

        self._ribout.write('RelativeDetail %s\n'%relativedetail)

    # RiDetailRange
    def RiDetailRange(self, minvisible, lowertransition, uppertransition, maxvisible):
        """Set the current detail range.

        The values of the parameters must satisfy the following ordering:
        minvisible <= lowertransition <= uppertransition <= maxvisible

                    lowertransition  uppertransition
     visibility         |____________________|       
        ^               /                    \\
        |              /                      \\
        |_____________/                        \\_____________\\ Level of detail
                     |                          |            /
                 minvisible                      maxvisible

        Example: RiDetailRange(0,0,10,20)
        """

        self._ribout.write('DetailRange %s %s %s %s\n'%(minvisible, lowertransition, uppertransition, maxvisible))

    # RiCoordinateSystem
    def RiCoordinateSystem(self, spacename):
        """Mark the current coordinate system with a name.

        Example: RiCoordinateSystem("lamptop")
        """
        self._ribout.write('CoordinateSystem "'+spacename+'"\n')

    # RiScopedCoordinateSystem
    def RiScopedCoordinateSystem(self, spacename):
        """Mark the current coordinate system with a name but store it on a separate stack.

        Example: RiScopedCoordinateSystem("lamptop")
        """
        self._ribout.write('ScopedCoordinateSystem "'+spacename+'"\n')

    # RiTransformPoints
    def RiTransformPoints(self, fromspace, tospace, points):
        """Transform a set of points from one space to another.

        This function is not implemented and always returns None.
        """

        return None

    # RiCoordSysTransform
    def RiCoordSysTransform(self, spacename):
        """Replace the current transformation matrix with spacename.

        Example: RiCoordSysTransform("lamptop")
        """

        self._ribout.write('CoordSysTransform "'+spacename+'"\n')

    # RiContext
    def RiContext(self, handle):
        """Set the current active rendering context.

        Example: ctx1 = RiGetContext()
                 ...
                 RiContext(ctx1)
        """

        self._switch_context(handle)

    # RiGetContext
    def RiGetContext(self):
        """Get a handle for the current active rendering context.

        Example: ctx1 = RiGetContext()
                 ...
                 RiContext(ctx1)"""

        return self._current_context

    # RiSystem
    def RiSystem(self, cmd):
        """Execute an arbitrary command in the same environment as the current rendering pass.
        """
        # Escape quotes
        cmd = cmd.replace('"', r'\"')
        self._ribout.write('System "%s"\n'%cmd)

    # RiIfBegin
    def RiIfBegin(self, expression, *paramlist, **keyparams):
        """Begin a conditional block.
        """
        self._ribout.write('IfBegin "%s"%s\n'%(expression, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiElseIf
    def RiElseIf(self, expression, *paramlist, **keyparams):
        """Add an else-if block to a conditional block.
        """
        
        self._ribout.write('ElseIf "%s"%s\n'%(expression, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiElse
    def RiElse(self):
        """Add an else block to a conditional block.
        """
        
        self._ribout.write('Else\n')

    # RiIfEnd
    def RiIfEnd(self):
        """Terminate a conditional block.
        """
        
        self._ribout.write('IfEnd\n')
        
    # RiResource
    def RiResource(self, handle, type, *paramlist, **keyparams):
        """Create or operate on a named resource of a particular type.
        """
        self._ribout.write('Resource "%s" "%s"%s\n'%(handle, type, riutils.paramlist2string(self, paramlist, keyparams)))

    # RiResourceBegin
    def RiResourceBegin(self):
        """Push the current set of resources. 
        """
        self._ribout.write('ResourceBegin\n')

    # RiResourceEnd
    def RiResourceEnd(self):
        """Pop the current set of resources. 
        """
        self._ribout.write('ResourceEnd\n')

    # If you're adding new global variables then make sure that they're
    # saved and loaded from the context handling functions and initialized
    # in RiBegin() and during the module initialization.

    ##################### Internal helper functions #######################

    def _save_context(self, handle):
        "Save a context."
        ctx = (self._ribout, self._colorsamples, self._lighthandle, self._objecthandle,
               self._errorhandler, self._declarations,
               self._insideframe, self._insideworld, self._insideobject, self._insidesolid,
               self._insidemotion)
        self._contexts[handle]=ctx

    def _load_context(self, handle):
        "Load a context."
        self._ribout, self._colorsamples, self._lighthandle, self._objecthandle, \
        self._errorhandler, self._declarations, \
        self._insideframe, self._insideworld, self._insideobject, self._insidesolid, \
        self._insidemotion = self._contexts[handle]

    def _create_new_context(self):
        "Create a new context and make it the active one."

        keys = self._contexts.keys()
        if len(keys)>0:
            handle = max(keys)+1
        else:
            handle = 1
        self._contexts[handle]=()
        
        if self._current_context!=None:
            self._save_context(self._current_context)

        self._current_context = handle

    def _switch_context(self, handle):
        "Save the current context and make another context the active one."
        
        if self._current_context!=None:
            self._save_context(self._current_context)
        self._current_context = handle
        self._load_context(handle)

    def _destroy_context(self):
        "Destroy the current active context"

        handle = self._current_context
        del self._contexts[handle]
        self._current_context = None

    def _init_declarations(self):
        self._declarations = {RI_P:"vertex point", RI_PZ:"vertex point",
                         RI_PW:"vertex hpoint",
                         RI_N:"varying normal", RI_NP:"uniform normal",
                         RI_CS:"varying color", RI_OS:"varying color",
                         RI_S:"varying float", RI_T:"varying float",
                         RI_ST:"varying float[2]",
                         RI_ORIGIN:"integer[2]",
                         RI_KA:"uniform float",
                         RI_KD:"uniform float",
                         RI_KS:"uniform float",
                         RI_ROUGHNESS:"uniform float",
                         RI_KR:"uniform float",
                         RI_TEXTURENAME:"string",
                         RI_SPECULARCOLOR:"uniform color",
                         RI_INTENSITY:"float",
                         RI_LIGHTCOLOR:"color",
                         RI_FROM:"point",
                         RI_TO:"point",
                         RI_CONEANGLE:"float",
                         RI_CONEDELTAANGLE:"float",
                         RI_BEAMDISTRIBUTION:"float",
                         RI_AMPLITUDE:"uniform float",
                         RI_MINDISTANCE:"float",
                         RI_MAXDISTANCE:"float",
                         RI_BACKGROUND:"color",
                         RI_DISTANCE:"float",
                         RI_FOV:"float",
                         RI_WIDTH:"varying float",
                         RI_CONSTANTWIDTH:"constant float",
                         "shader":"string",
                         "archive":"string",
                         "texture":"string",
                         "procedural":"string",
                         "endofframe":"integer",
                         "sphere":"float",
                         "coordinatesystem":"string",
                         "name":"string",
                         "sense":"string"
                        }

    def _error(self, code, severity, message):

        RiLastError = code

        st = inspect.stack(1)
        # Search the offending Ri function in the stack...
        j=None
        for i in range(len(st)):
            if st[i][3][:2]=="Ri":
                j=i
        # No function beginning with "Ri" found? That's weird. Maybe someone
        # messed with the function names.
        if j==None:
            where=""
        else:
            # name of the Ri function
            call   = inspect.stack(0)[j][3]
            # filename and line number where the offending Ri call occured
            file   = inspect.stack(1)[j+1][1]
            line   = inspect.stack(1)[j+1][2]
            if file==None: file="?"
            where = 'In file "'+file+'", line '+`line`+' - '+call+"():\n"

        self._errorhandler(code,severity,where+message)

if __name__=='__main__':

    RiBegin(RI_NULL)
    RiErrorHandler(RiErrorAbort)

    RiWorldBegin();

    RiWorldEnd()

    RiSkew(45,0,1,0,1,0,0)
    RiSkew(45,[0,1,0],[1,0,0])
    
    RiEnd()
    
