import sys, types, time, os, os.path, string, getpass, inspect, gzip
import ri
#try:
    #from _core import vec3 as _vec3
#except:
    #from cgtypes import vec3 as _vec3

########################### Constants #############################

NULL         = None

TRUE         = 1
FALSE        = 0

HIDDEN       = "hidden"
PAINT        = "paint"

EPSILON      = 1.0e-10
INFINITY     = 1.0e38

FILE         = "file"
FRAMEBUFFER  = "framebuffer"
RGB          = "rgb"
RGBA         = "rgba"
RGBZ         = "rgbZ"
RGBAZ        = "rgbaz"
A            = "a"
Z            = "z"
AZ           = "az"

ORIGIN       = "origin"

PERSPECTIVE  = "perspective"
ORTHOGRAPHIC = "orthographic"
FOV          = "fov"

LH           = "lh"
RH           = "rh"
INSIDE       = "inside"
OUTSIDE      = "outside"

BILINEAR     = "bilinear"
BICUBIC      = "bicubic"

LINEAR       = "linear"
CUBIC        = "cubic"

CONSTANT     = "constant"
SMOOTH       = "smooth"

P            = "P"
PW           = "Pw"
PZ           = "Pz"
N            = "N"
NP           = "Np"
NG           = "Ng"
CI           = "Ci"
OI           = "Oi"
CS           = "Cs"
OS           = "Os"
S            = "s"
T            = "t"
ST           = "st"

COMMENT      = "comment"
STRUCTURE    = "structure"
VERBATIM     = "verbatim"

HERMITESTEP    = 2
CATMULLROMSTEP = 1
BEZIERSTEP     = 3
BSPLINESTEP    = 1
POWERSTEP      = 4

PERIODIC     = "periodic"
NONPERIODIC  = "nonperiodic"
CLAMP        = "clamp"
BLACK        = "black"

FLATNESS     = "flatness"

PRIMITIVE    = "primitive"
UNION        = "union"
DIFFERENCE   = "difference"
INTERSECTION = "intersection"

WIDTH        = "width"
CONSTANTWIDTH = "constantwidth"

HOLE         = "hole"
CREASE       = "crease"
CORNER       = "corner"
INTERPOLATEBOUNDARY = "interpolateboundary"

AMBIENTLIGHT = "ambientlight"
POINTLIGHT   = "pointlight"
DISTANTLIGHT = "distantlight"
SPOTLIGHT    = "spotlight"

INTENSITY    = "intensity"
LIGHTCOLOR   = "lightcolor"
FROM         = "from"
TO           = "to"
CONEANGLE    = "coneangle"
CONEDELTAANGLE = "conedeltaangle"
BEAMDISTRIBUTION = "beamdistribution"

MATTE        = "matte"
METAL        = "metal"
SHINYMETAL   = "shinymetal"
PLASTIC      = "plastic"
PAINTEDPLASTIC = "paintedplastic"

KA           = "Ka"
KD           = "Kd"
KS           = "Ks"
ROUGHNESS    = "roughness"
KR           = "Kr"
TEXTURENAME  = "texturename"
SPECULARCOLOR = "specularcolor"

DEPTHCUE     = "depthcue"
FOG          = "fog"
BUMPY        = "bumpy"

MINDISTANCE  = "mindistance"
MAXDISTANCE  = "maxdistance"
BACKGROUND   = "background"
DISTANCE     = "distance"
AMPLITUDE    = "amplitude"

RASTER       = "raster"
SCREEN       = "screen"
CAMERA       = "camera"
WORLD        = "world"
OBJECT       = "object"

IDENTIFIER   = "identifier"
NAME         = "name"
SHADINGGROUP = "shadinggroup"

IGNORE       = "ignore"
PRINT        = "print"
ABORT        = "abort"
HANDLER      = "handler"

HANDLEID     = "__handleid"

# Tokens specific to the cgkit binding...
RIBOUTPUT    = "_riboutput"
VERSION      = "_version"

# Error handling: severity levels
RIE_INFO        = 0
RIE_WARNING     = 1
RIE_ERROR       = 2
RIE_SEVERE      = 3

RIE_INCAPABLE   = 11

RIE_NOTOPTIONS  = 25       # Invalid state for options
RIE_NOTATTRIBS  = 26       # Invalid state for attributes
RIE_NOTPRIMS    = 27       # Invalid state for primitives
RIE_ILLSTATE    = 28       # Other invalid state 
RIE_RANGE       = 42       # Parameter out of range 
RIE_CONSISTENCY = 43       # Parameters inconsistent

RIE_INVALIDSEQLEN = 80     # A sequence hasn't had the required length
RIE_UNDECLARED    = 81     # An undeclared parameter is used

LastError     = 0

############################ Types ###################################

RtBoolean = bool
RtInt = int
RtFloat = float
RtString = str
RtToken = str
RtVoid = None
RtPointer = lambda x: x

RtColor = tuple
RtPoint = tuple
RtVector = tuple
RtNormal = tuple
RtHpoint = tuple
RtMatrix = tuple
RtBasis = tuple
RtBound = tuple

RtObjectHandle = lambda x: x
RtLightHandle = lambda x: x
RtContextHandle = lambda x: x

RtFilterFunc = lambda x: x
RtErrorHandler = lambda x: x
RtProcSubdivFunc = lambda x: x
RtProcFreeFunc = lambda x: x
RtArchiveCallback = lambda x: x


######################################################################

class RIBStream:
    """This class encapsulates the output stream.

    The version number is automatically placed into the stream before
    any "real"  calls are made. Output from ArchiveRecord() will
    be placed before the version number. (Note: The version line is disabled
    for now).
    """
    
    def __init__(self, outstream):
        self.out = outstream
        self.output_version = 1

    def close(self):
        """Close the stream, unless it's stdout."""
        if self.out!=sys.stdout:
            self.out.close()

    def flush(self):
        """Flush the internal buffer."""
        self.out.flush()

    def write(self, data):
        """Write data into the stream."""
        if self.output_version:
            # The binding contains newer calls, so this version number
            # might not be accurate anyway.
#            self.out.write('version 3.03\n')
            self.output_version = 0
        self.out.write(data)

    def writeArchiveRecord(self, data):
        """Same as write() but suppresses the version number.

        This method is used by ArchiveRecord(), everyone else uses
        write().
        """
        self.out.write(data)
        

###################### Standard error handlers #######################

def ErrorIgnore(code, severity, message):
    """Standard error handler.

    Ignores error messages."""
    
    pass

def ErrorPrint(code, severity, message):
    """Standard error handler.

    Prints the message to stderr."""

    if severity==RIE_WARNING:
        print >> sys.stderr, "WARNING:",
    elif severity==RIE_ERROR or severity==RIE_SEVERE:
        print >> sys.stderr, "ERROR (%d):"%(code),        
    print >> sys.stderr, message

def ErrorAbort(code, severity, message):
    """Standard error handler.

    Prints the message to stderr and aborts if it was an error."""

    ErrorPrint(code, severity, message)
    if severity>=RIE_ERROR:
        sys.exit(1)


class RIException(Exception):
    """RenderMan Interface exception

    This exception is thrown by the error handler ErrorException()."""
    pass

def ErrorException(code, severity, message):
    """This error handler raises an exception when an error occurs.

    If the "error" is only an info or warning message the message is
    printed to stderr, otherwise the exception RIException is thrown.
    The actual error message is given as an argument to the constructor of
    RIException (the line with the file name, line number and offending
     call is removed. You will have that information in the Traceback).
    """
    if severity<RIE_ERROR:
        ErrorPrint(code, severity, message)
    else:
        if message[:7]=="In file":
            n=message.find("\n")
            message=message[n+1:]
        raise RIException(message)

########################### Functions ################################

# ErrorHandler
def ErrorHandler(handler):
    """Install a new error handler.

    The handler takes three arguments: code, severity, message.
    Besides the three standard error handler ErrorIgnore, ErrorPrint
    and ErrorAbort there's an additional error handler available called
    ErrorException. Whenever an error occurs ErrorException raises
    the exception RIException.

    If you use one of the standard error handlers the corresponding RIB
    request is written to the output. If you supply ErrorException or
    your own handler then the handler is installed but no output is
    written to the output stream.

    The last error code is always stored in the variable LastError.
    Note: If you import the module with "from ri import *" you have to
    import it with "import ri" as well and you must access LastError
    via "ri.LastError" otherwise the variable will always be 0.

    Example: ErrorHandler(ErrorAbort)
    """

    global _errorhandler

    _errorhandler = handler

    if handler==ErrorIgnore:
        _ribout.write('ErrorHandler "ignore"\n')
    elif handler==ErrorPrint:
        _ribout.write('ErrorHandler "print"\n')
    elif handler==ErrorAbort:
        _ribout.write('ErrorHandler "abort"\n')


# Begin
def Begin(name):
    """Starts the main block using a particular rendering method.
    
    The default renderer is selected by passing NULL as name.
    Here this means the output is written to stdout.
    If the name has the extension ".rib" then the output is written into
    a file with that name. Otherwise the name is supposed to be an
    external renderer (e.g. "rendrib" (BMRT), "rgl" (BMRT), "aqsis" (Aqsis),
    "renderdl" (3Delight),...) which is started and fed with the data.

    Example: Begin(NULL)
             ...
             End()
    """
    global _ribout, _colorsamples, _lighthandle, _errorhandler
    global _insideframe, _insideworld, _insideobject, _insidesolid
    global _insidemotion, _declarations

    _create_new_context()

    # Determine where the output should be directed to...
    if name==NULL or name=="":
        # -> stdout
        outstream = sys.stdout
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

    _ribout = RIBStream(outstream)

    # Initialize internal variables
    _colorsamples = 3
    _lighthandle  = 0
    _errorhandler = ErrorPrint
    _insideframe  = 0
    _insideworld  = 0
    _insideobject = 0
    _insidesolid  = 0
    _insidemotion = 0
    _init_declarations()


# End
def End():
    """Terminates the main block.
    """
    global _ribout

    _ribout.flush()
    
    if _ribout != sys.stdout:
        _ribout.close()
        _ribout = sys.stdout

    _destroy_context()

# WorldBegin
def WorldBegin():
    """Start the world block.

    Example: WorldBegin()
             ...
             WorldEnd()
    """

    global _insideworld

    if _insideworld:
        _error(RIE_ILLSTATE, RIE_ERROR, "World blocks cannot be nested.")
    
    # _ribout.write('Option "statistics" "endofframe" [1] "filename" ["stats.txt"] "xmlfilename" ["stats.xml"]\n')
    _ribout.write("WorldBegin\n")
    _insideworld = 1

# WorldEnd
def WorldEnd():
    """Terminates the world block."""

    global _insideworld
    
    _ribout.write("WorldEnd\n")
    _insideworld = 0

# Option
def Option(name, *paramlist, **keyparams):
    """Set an implementation-specific option.

    Example: Option("searchpath", "shader","~/shaders:&")
    """
    global _ribout

    # cgkit specific options?
    if name==RIBOUTPUT:
        keyparams = _paramlist2lut(paramlist, keyparams)
        if keyparams.get(VERSION, None)==0:
            # Disable the "version" call in the RIB stream...
            if hasattr(_ribout, "output_version"):
                _ribout.output_version = 0
        return
            
    _ribout.write('Option "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Attribute
def Attribute(name, *paramlist, **keyparams):
    """Set an implementation-specific attribute.

    Example: Attribute("displacementbound", "sphere", 0.5)
    """
    
    _ribout.write('Attribute "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# AttributeBegin
def AttributeBegin():
    """Push the current set of attributes onto the attribute stack.

    Example: AttributeBegin()
             ...
             AttributeEnd()
    """
    
    _ribout.write("AttributeBegin\n")

# AttributeEnd
def AttributeEnd():
    """Pops the current set of attributes from the attribute stack."""

    _ribout.write("AttributeEnd\n")

# TransformBegin
def TransformBegin():
    """Push the current transformation on the transformation stack.

    Example: TransformBegin()
             ...
             TransformEnd()
    """
    
    _ribout.write("TransformBegin\n")

# TransformEnd
def TransformEnd():
    """Pop the current transformation from the stack."""

    _ribout.write("TransformEnd\n")

# FrameBegin
def FrameBegin(number):
    """Start a new frame.

    Example: FrameBegin(1)
             ...
             FrameEnd()
    """

    global _insideframe

    if _insideframe:
        _error(RIE_ILLSTATE, RIE_ERROR, "Frame blocks cannot be nested.")
            
    _ribout.write("FrameBegin %d\n"%number)
    _insideframe = 1
    

# FrameEnd
def FrameEnd():
    """Terminates a frame."""
    
    global _insideframe
    
    _ribout.write("FrameEnd\n")
    _insideframe = 0

# Hider
def Hider(type, *paramlist, **keyparams):
    """Choose a hidden-surface elimination technique.

    Example: Hider(HIDDEN)  (default)
    """
    
    if type==NULL: type="null"
    _ribout.write('Hider "'+type+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Sphere
def Sphere(radius,zmin,zmax,thetamax,*paramlist, **keyparams):
    """Create a sphere.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Sphere(1.0, -1.0, 1.0, 360)
    """

    _ribout.write('Sphere %s %s %s %s'%(radius, zmin, zmax, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Cone
def Cone(height, radius, thetamax, *paramlist, **keyparams):
    """Create a cone (along the z axis).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Cone(1.5, 0.7, 360)
    """

    _ribout.write('Cone %s %s %s'%(height, radius, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Disk
def Disk(height, radius, thetamax, *paramlist, **keyparams):
    """Create a disk (parallel to the XY plane).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Disk(0.0, 1.0, 360)"""

    _ribout.write('Disk %s %s %s'%(height, radius, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Cylinder
def Cylinder(radius,zmin,zmax,thetamax,*paramlist, **keyparams):
    """Create a cylinder (along the z axis).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Cylinder(1.5, 0.0, 1.0, 360)
    """

    _ribout.write('Cylinder %s %s %s %s'%(radius, zmin, zmax, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Torus
def Torus(major, minor, phimin, phimax, thetamax, *paramlist, **keyparams):
    """Create a torus (with the z axis as symmetry axis).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Torus(1.5, 0.1, 0, 360, 360)
    """

    _ribout.write('Torus %s %s %s %s %s'%(major, minor, phimin, phimax, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Hyperboloid
def Hyperboloid(point1, point2, thetamax, *paramlist, **keyparams):
    """Create a hyperboloid (with the z axis as symmetry axis).

    Example: Hyperboloid([1,0,0],[1,1,1],360)
    """

    p1 = _seq2list(point1, 3)
    p2 = _seq2list(point2, 3)
    _ribout.write('Hyperboloid '+p1[1:-1]+' '+p2[1:-1]+' '+`thetamax`+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Paraboloid
def Paraboloid(rmax, zmin, zmax, thetamax, *paramlist, **keyparams):
    """Create a paraboloid (with the z axis as symmetry axis).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4

    Example: Paraboloid(1.0, 0.0, 1.0, 360)
    """

    _ribout.write('Paraboloid %s %s %s %s'%(rmax, zmin, zmax, thetamax)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Polygon
def Polygon(*paramlist, **keyparams):
    """Create a planar and convex polygon.

    The parameter list must include at least position ("P") information.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #vertices
    uniform:  1              vertex:  #vertices

    Example: Polygon(P=[0,1,0, 0,1,1, 0,0,1, 0,0,0])
    """

    _ribout.write('Polygon'+_paramlist2string(paramlist, keyparams)+"\n")

# GeneralPolygon
def GeneralPolygon(nverts, *paramlist, **keyparams):
    """Create a general planar concave polygon with holes.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #total vertices
    uniform:  1              vertex:  #total vertices

    Example: GeneralPolygon([4,3], P=[0,0,0, 0,1,0, 0,1,1, 0,0,1, \\
                                        0,0.25,0.5, 0,0.75,0.75, 0,0.75,0.25])
    """

    _ribout.write('GeneralPolygon '+_seq2list(nverts)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# PointsPolygons
def PointsPolygons(nverts, vertids, *paramlist, **keyparams):
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

    _ribout.write('PointsPolygons '+_seq2list(nverts)+' '+ \
                 _seq2list(vertids)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# PointsGeneralPolygons
def PointsGeneralPolygons(nloops, nverts, vertids, *paramlist, **keyparams):
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

    _ribout.write('PointsGeneralPolygons '+_seq2list(nloops)+' '+ \
                 _seq2list(nverts)+' '+_seq2list(vertids)+ \
                 _paramlist2string(paramlist, keyparams)+"\n")


# Predefined basis matrices
HermiteBasis = "hermite"
CatmullRomBasis = "catmull-rom"
BezierBasis = "bezier"
BSplineBasis = "b-spline"
PowerBasis = "power"

# Basis
def Basis(ubasis, ustep, vbasis, vstep):
    """Set the current basis for the u and v direction.

    ubasis/vbasis can either be one of the predefined basis matrices
    HermiteBasis, CatmullRomBasis, BezierBasis, BSplineBasis,
    PowerBasis or it can be a user defined matrix.

    For the predefined matrices there are also predefined variables
    which can be used for the step parameters:
    HERMITESTEP, CATMULLROMSTEP, BEZIERSTEP, BSPLINESTEP,
    POWERSTEP.

    Example: Basis(BezierBasis, BEZIERSTEP,
                     HermiteBasis, HERMITESTEP)
    """

    if type(ubasis)==types.StringType:
        ubasis = '"'+ubasis+'"'
    else:
        ubasis = _seq2list(ubasis, 16)
        
    if type(vbasis)==types.StringType:
        vbasis = '"'+vbasis+'"'
    else:
        vbasis = _seq2list(vbasis, 16)
        
    _ribout.write('Basis '+ubasis+' '+str(ustep)+' '+vbasis+' '+str(vstep)+"\n")

# Patch
def Patch(type, *paramlist, **keyparams):
    """Patch(type, paramlist)

    type is one of BILINEAR (4 vertices) or BICUBIC (16 vertices).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: 4
    uniform:  1              vertex:  4/16 (depends on type)

    Example: Patch(BILINEAR, P=[0,0,0, 1,0,0, 0,1,0, 1,1,0])
    """

    _ribout.write('Patch "'+type+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# PatchMesh
def PatchMesh(type, nu, uwrap, nv, vwrap, *paramlist, **keyparams):
    """Create a mesh made of patches.

    type is one of BILINEAR or BICUBIC.
    uwrap/vwrap can be PERIODIC or NONPERIODIC.
    The number of control points is nu*nv.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #patch corners (depends on uwrap/vwrap)
    uniform:  #patches       vertex:  nu*nv (same as "P")

    """

    _ribout.write('PatchMesh "'+type+'" '+str(nu)+' "'+uwrap+'" '+\
                 str(nv)+' "'+vwrap+'"'+\
                 _paramlist2string(paramlist, keyparams)+"\n")
    

# NuPatch
def NuPatch(nu, uorder, uknot, umin, umax, nv, vorder, vknot, vmin, vmax, *paramlist, **keyparams):
    """Create a NURBS patch.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #segment corners
    uniform:  #segments      vertex:  nu*nv
    """

    _ribout.write('NuPatch '+str(nu)+" "+str(uorder)+' '+_seq2list(uknot)+" "+ \
                 str(umin)+" "+str(umax)+" "+ \
                str(nv)+" "+str(vorder)+' '+_seq2list(vknot)+" "+ \
                 str(vmin)+" "+str(vmax)+_paramlist2string(paramlist, keyparams)+"\n")

# TrimCurve
def TrimCurve(ncurves, order, knot, min, max, n, u, v, w):
    """Set the current trim curve.
    """

    _ribout.write('TrimCurve '+_seq2list(ncurves)+' '+\
                 _seq2list(order)+' '+_seq2list(knot)+' '+\
                 _seq2list(min)+' '+_seq2list(max)+' '+_seq2list(n)+' '+ \
                 _seq2list(u)+' '+ \
                 _seq2list(v)+' '+ \
                 _seq2list(w)+'\n')

# Points
def Points(*paramlist, **keyparams):
    """Create individual points.

    The size of the points can be either set with the primitive variable
    WIDTH (one float per point) or CONSTANTWIDTH (one float for all
    points).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #points
    uniform:  1              vertex:  #points    
    """

    _ribout.write('Points'+_paramlist2string(paramlist, keyparams)+"\n")

# Curves
def Curves(type, nvertices, wrap, *paramlist, **keyparams):
    """Create a number of curve primitives.

    type is either LINEAR or CUBIC.
    nvertices is an array with the number of vertices in each curve.
    wrap is either PERIODIC or NONPERIODIC.
    The width of the curves can be specified with the parameter
    WIDTH (varying float) or CONSTANTWIDTH (constant float).

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: #segments (depends on type and wrap)
    uniform:  #curves        vertex:  #points

    Example: Curves(CUBIC, [4], NONPERIODIC,
                      P=[0,0,0, -1,-0.5,1, 2,0.5,1, 1,0,-1],
                      width=[0.1, 0.04])
    """

    _ribout.write('Curves "'+type+'" '+_seq2list(nvertices)+' "'+wrap+'"'+
                  _paramlist2string(paramlist, keyparams)+'\n')

# SubdivisionMesh
def SubdivisionMesh(scheme, nverts, vertids, tags, nargs, intargs, floatargs, *paramlist, **keyparams):
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
        _ribout.write('SubdivisionMesh "'+scheme+'" '+_seq2list(nverts)+' '+ \
                 _seq2list(vertids)+' '+ \
                 _paramlist2string(paramlist, keyparams)+"\n")
    else:
        _ribout.write('SubdivisionMesh "'+scheme+'" '+_seq2list(nverts)+' '+ \
                 _seq2list(vertids)+' '+_seq2list(tags)+' '+ \
                 _seq2list(nargs)+' '+_seq2list(intargs)+' '+ \
                 _seq2list(floatargs)+' '+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Blobby
def Blobby(nleaf, code, floats, strings, *paramlist, **keyparams):
    """Create a blobby surface.

    Number of array elements for primitive variables:
    -------------------------------------------------
    constant: 1              varying: nleaf
    uniform:  1              vertex:  nleaf

    Example: Blobby(2, [1001,0, 1003,0,16, 0,2,0,1],
                      [1.5,0,0,0, 0,1.5,0,0, 0,0,1.5,0, 0,0,-.1,1,
                      0.4, 0.01,0.3, 0.08], ["flat.zfile"])
    """

    _ribout.write('Blobby '+str(nleaf)+' '+_seq2list(code)+' '+_seq2list(floats)+
                  ' '+_seq2list(strings)+
                  _paramlist2string(paramlist, keyparams)+'\n')

### new geometry
#RiVolume
def Volume(typename, bounds, nvertices, *paramlist, **keyparams):
    ri.RiVolume(typename, bounds, nvertices, *paramlist, **keyparams)
### 

# ColorSamples
def ColorSamples(nRGB, RGBn):
    """Redefine the number of color components to be used for specifying colors.

    nRGB is a n x 3 matrix that can be used to transform the n component color
    to a RGB color (n -> RGB).
    RGBn is just the opposite, its a 3 x n matrix that's used to transform
    a RGB color to a n component color (RGB -> n).
    Thus, the new number of color components is len(matrix)/3 (matrix is
    either nRGB or RGBn).

    Example: ColorSamples([0.3,0.3,0.3], [1,1,1])
    """
    global _colorsamples

    if len(nRGB)!=len(RGBn):
        _error(RIE_CONSISTENCY, RIE_ERROR,
               "The color transformation matrices must have the same number of values.")

    if len(nRGB)%3!=0 or len(nRGB)==0:
        _error(RIE_CONSISTENCY, RIE_ERROR,
               "The number of values in the transformation matrices must be a multiple of 3.")
        
    _colorsamples = len(_flatten(nRGB))/3
    _ribout.write('ColorSamples '+_seq2list(nRGB)+' '+_seq2list(RGBn)+'\n')

# Color
def Color(Cs):
    """Set the current color.

    Cs must be a sequence of at least N values where N is the number of
    color samples (set by ColorSamples(), default is 3).

    Example: Color([0.2,0.5,0.2])
    """

    col=_seq2col(Cs)
    _ribout.write("Color "+col+"\n")

# Opacity
def Opacity(Os):
    """Set the current opacity.

    Os must be a sequence of at least N values where N is the number
    of color samples (set by ColorSamples(), default is 3). The
    opacity values must lie in the range from 0 to 1 (where 0 means
    completely transparent and 1 means completely opaque).

    Example: Opacity([0,0,1])
    """

    col=_seq2col(Os)
    _ribout.write("Opacity "+col+"\n")

# ShadingRate
def ShadingRate(size):
    """Set the current shading rate to an area of size pixels.

    Example: ShadingRate(1.0)
    """

    _ribout.write("ShadingRate %s\n"%size)

# ShadingInterpolation
def ShadingInterpolation(type):
    """Specify how shading samples are interpolated.

    type can be CONSTANT or SMOOTH.

    Example: ShadingInterpolation(SMOOTH)"""

    _ribout.write('ShadingInterpolation "'+type+'"\n')

# Shader
def Shader(name, handle, *paramlist, **keyparams):
    """Set the current coshader.

    Example: Shader("plastic", "plastic_layer", Kd=0.7, Ks=0.3)"""

    _ribout.write('Shader "'+name+'"'+' "'+handle+'"'+ \
                 _paramlist2string(paramlist, keyparams)+"\n")
    
# Surface
def Surface(name, *paramlist, **keyparams):
    """Set the current surface shader.

    Example: Surface("plastic", Kd=0.7, Ks=0.3)"""

    _ribout.write('Surface "'+name+'"'+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# Interior
def Interior(name, *paramlist, **keyparams):
    """Set the current interior volume shader.

    Example: Interior("water")
    """

    _ribout.write('Interior "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Exterior
def Exterior(name, *paramlist, **keyparams):
    """Set the current exterior volume shader.

    Example: Exterior("fog")
    """

    _ribout.write('Exterior "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Atmosphere
def Atmosphere(name, *paramlist, **keyparams):
    """Set the current atmosphere shader.

    If name is NULL then no atmosphere shader is used.

    Example: Atmosphere("fog")
    """

    if name==NULL:
        _ribout.write('Atmosphere\n')
    else:
        _ribout.write('Atmosphere "'+name+'"'+ \
                      _paramlist2string(paramlist, keyparams)+"\n")

# Displacement
def Displacement(name, *paramlist, **keyparams):
    """Set the current displacement shader.

    Example: Displacement("dented", km=1.5)
    """

    _ribout.write('Displacement "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Imager
def Imager(name, *paramlist, **keyparams):
    """Set an imager shader.

    if name is NULL, no imager shader is used.

    Example: Imager("background", "color bgcolor", [0.3,0.3,0.9])
    """

    if name==NULL:
        _ribout.write('Imager\n')
    else:
        _ribout.write('Imager "'+name+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Clipping
def Clipping(near, far):
    """Sets the near and the far clipping plane along the direction of view.

    near and far must be positive values in the range from EPSILON to
    INFINITY.

    Example: Clipping(0.1, 100)
    """

    _ribout.write("Clipping %s %s\n"%(near,far))

# ClippingPlane
def ClippingPlane(x, y, z, nx, ny, nz):
    """Adds a new clipping plane, defined by a surface point and its normal.

    All the geometry in positive normal direction is clipped.

    Example: ClippingPlane(0,0,0, 0,0,-1) clips everything below the XY plane
    """

    _ribout.write('ClippingPlane %s %s %s %s %s %s\n'%(x,y,z,nx,ny,nz))

# Display
def Display(name,type,mode, *paramlist, **keyparams):
    """Specify the destination and type of the output.

    Example: Display("frame0001.tif", FILE, RGB)
             Display("myimage.tif", FRAMEBUFFER, RGB)
    """

    _ribout.write('Display "'+name+'" "'+type+'" "'+mode+'"'+ \
                 _paramlist2string(paramlist, keyparams)+"\n")

# DisplayChannel
def DisplayChannel(channel, *paramlist, **keyparams):
    """Defines a new display channel.

    Example: DisplayChannel("color aovCi", "string opacity", "aovOi")
    """
    _ribout.write('DisplayChannel "%s"%s\n'%(channel, _paramlist2string(paramlist, keyparams)))

# Format
def Format(xres, yres, aspect):
    """Set the resolution of the output image and the aspect ratio of a pixel.

    Example: Format(720,576,1)"""

    _ribout.write('Format %s %s %s\n'%(xres, yres, aspect))

# FrameAspectRatio
def FrameAspectRatio(frameratio):
    """Set the ratio between width and height of the image.

    Example: FrameAspectRatio(4.0/3)
    """

    _ribout.write('FrameAspectRatio %s\n'%frameratio)

# GeometricApproximation
def GeometricApproximation(type, value):
    """Sets parameters for approximating surfaces.

    Example: GeometricApproximation(FLATNESS, 0.5)  (default value)
    """

    _ribout.write('GeometricApproximation "'+type+'" '+str(value)+"\n")


# Projection
def Projection(name, *paramlist, **keyparams):
    """Specify a projection method.

    The standard projections are PERSPECTIVE and ORTHOGRAPHIC.
    The perspective projection takes one optional parameter, FOV.

    Example: Projection(PERSPECTIVE, fov=45)
    """

    if name==NULL:
        _ribout.write('Projection\n')
    else:
        _ribout.write('Projection "'+name+'"'+ \
                      _paramlist2string(paramlist, keyparams)+"\n")

# Camera
def Camera(name, *paramlist, **keyparams):
    """Mark the current camera description.

    Example: Camera("rightcamera")
    """
    _ribout.write('Camera "%s"%s\n'%(name, _paramlist2string(paramlist, keyparams)))

# ScreenWindow
def ScreenWindow(left, right, bottom, top):
    """Specify the extents of the output image on the image plane.

    Example: ScreenWindow(-1,1,-1,1)
    """

    _ribout.write('ScreenWindow %s %s %s %s\n'%(left, right, bottom, top))

# CropWindow
def CropWindow(left, right, bottom, top):
    """Specify a subwindow to render.

    The values each lie between 0 and 1.

    Example: CropWindow(0.0, 1.0 , 0.0, 1.0)  (renders the entire frame)
             CropWindow(0.5, 1.0 , 0.0, 0.5)  (renders the top right quarter)
    """

    _ribout.write('CropWindow %s %s %s %s\n'%(left, right, bottom, top))

# PixelSamples
def PixelSamples(xsamples, ysamples):
    """Set the sampling rate in horizontal and vertical direction.

    Example: PixelSamples(2,2)"""

    _ribout.write("PixelSamples %s %s\n"%(max(1,xsamples), max(1,ysamples)))

# PixelVariance
def PixelVariance(variance):
    """Limit the acceptable variance in the output value of pixels.

    Example: PixelVariance(0.01)"""

    _ribout.write('PixelVariance %s\n'%variance)

# Predefined filter functions:
GaussianFilter   = "gaussian"
BoxFilter        = "box"
TriangleFilter   = "triangle"
SincFilter       = "sinc"
CatmullRomFilter = "catmull-rom"

# PixelFilter
def PixelFilter(function, xwidth, ywidth):
    """Set a pixel filter function and its width in pixels.

    Note: Here you can only use one of the predefined filter functions:
    GaussianFilter, BoxFilter, TriangleFilter, SincFilter and
    CatmullRomFilter.
    Passing a callable as filter function will issue a warning and ignore
    the call.

    Example: PixelFilter(GaussianFilter, 2.0, 1.0)"""
    
    if callable(function):
        _error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
        return

    _ribout.write('PixelFilter "'+function+'" '+str(xwidth)+' '+str(ywidth)+'\n')

# Exposure
def Exposure(gain, gamma):
    """Sets the parameters for the output color transformation.

    The transformation is color_out = (color_in*gain)^(1/gamma)

    Example: Exposure(1.3, 2.2)
    """

    _ribout.write("Exposure %s %s\n"%(gain, gamma))

# Quantize
def Quantize(type, one, min, max, ditheramplitude):
    """Set the quantization parameters for colors and depth.

    Example: Quantize(RGBA, 2048, -1024, 3071, 1.0)
    """

    _ribout.write('Quantize "%s" %s %s %s %s\n'%(type, one, min, max, ditheramplitude))
    

# DepthOfField
def DepthOfField(fstop, focallength, focaldistance):
    """Set depth of field parameters.

    If fstop is INFINITY depth of field is turned off.

    Example: DepthOfField(22,45,1200)
    """

    if fstop==INFINITY:
        _ribout.write('DepthOfField\n')
    else:
        _ribout.write('DepthOfField %s %s %s\n'%(fstop, focallength, focaldistance))

# MotionBegin
def MotionBegin(*times):
    """Start the definition of a moving primitive.

    You can specify the time values directly or inside a sequence,
    for example, MotionBegin(0,1) or MotionBegin([0,1]).

    Example: MotionBegin(0.0, 1.0)
             Translate(1.0, 0.0, 0.0)
             Translate(1.0, 2.0, 0.0)
             MotionEnd()
    """

    global _insidemotion

    if _insidemotion:
        _error(RIE_ILLSTATE, RIE_ERROR, "Motion blocks cannot be nested.")

    _ribout.write('MotionBegin '+_seq2list(times)+'\n')
    _insidemotion = 1

# MotionEnd
def MotionEnd():
    "Terminates the definition of a moving primitive."

    global _insidemotion

    _ribout.write('MotionEnd\n')
    _insidemotion = 0

# Shutter
def Shutter(opentime, closetime):
    """Set the times at which the shutter opens and closes.

    Example: Shutter(0.1, 0.9)
    """

    _ribout.write('Shutter %s %s\n'%(opentime, closetime))

# Translate
def Translate(*translation):
    """Concatenate a translation onto the current transformation.

    The translation is either given as 3 scalars or a sequence of
    3 scalars.

    Example: Translate(1.2, 4.3, -0.5)
             or
             Translate( (1.2, 4.3, -0.5) )
    """

    # Argument = sequence?
    if len(translation)==1:
        s=_seq2list(translation,3)
        _ribout.write('Translate '+s[1:-1]+"\n")
    # Argument = 3 scalars?
    elif len(translation)==3:
        dx,dy,dz=translation
        _ribout.write('Translate %s %s %s\n'%(dx,dy,dz))
    # Invalid argument size
    else:
        raise TypeError, "Translate() only takes a sequence or three scalars as arguments"

# Rotate
def Rotate(angle, *axis):
    """Rotate about angle degrees about the given axis.

    The axis is either given as 3 scalars or a sequence of 3 scalars.

    Example: Rotate(90, 1,0,0)
    """

    # Argument = sequence?
    if len(axis)==1:
        s=_seq2list(axis,3)
        _ribout.write('Rotate %s %s\n'%(angle, s[1:-1]))
    # Argument = 3 scalars?
    elif len(axis)==3:
        ax,ay,az=axis
        _ribout.write('Rotate %s %s %s %s\n'%(angle, ax, ay, az))
    # Invalid argument size
    else:
        raise TypeError, "Rotate() only takes 2 or 4 arguments ("+`len(axis)+1`+" given)"


# Scale
def Scale(*scaling):
    """Concatenate a scaling onto the current transformation.

    The scaling is either given as 3 scalars or a sequence of 3 scalars.

    Example: Scale(2,2,2)"""

    # Argument = sequence?
    if len(scaling)==1:
        s=_seq2list(scaling,3)
        _ribout.write('Scale '+s[1:-1]+"\n")
    # Argument = 3 scalars?
    elif len(scaling)==3:
        sx,sy,sz=scaling
        _ribout.write('Scale %s %s %s\n'%(sx, sy, sz))
    # Invalid argument size
    else:
        raise TypeError, "Scale() only takes a sequence or three scalars as arguments"


# Skew
def Skew(angle, *vecs):
    """Concatenate a skew onto the current transformation.

    angle is given in degrees.
    The two vectors are each given as 3 scalars or a sequence
    of 3 scalars.

    Example: Skew(45, 0,1,0, 1,0,0)
    """

    # Argument = two sequences?
    if len(vecs)==2:
        s1=_seq2list(vecs[0],3)
        s2=_seq2list(vecs[1],3)
        _ribout.write('Skew '+str(angle)+" "+s1[1:-1]+" "+s2[1:-1]+"\n")
    # Argument = 6 scalars?
    elif len(vecs)==6:
        dx1,dy1,dz1,dx2,dy2,dz2=vecs
        _ribout.write('Skew %s %s %s %s %s %s %s\n'%(angle, dx1, dy1, dz1, dx2, dy2, dz2))
    # Invalid argument size
    else:
        raise TypeError, "Skew() only takes 3 or 7 arguments ("+`len(vecs)+1`+" given)"


# Perspective
def Perspective(fov):
    """Concatenate a perspective transformation onto the current transformation.
    
    Example: Perspective(45)"""

    _ribout.write('Perspective %s\n'%fov)

# Identity
def Identity():
    """Set the current transformation to the identity.

    Example: Identity()
    """

    _ribout.write('Identity\n')

# ConcatTransform
def ConcatTransform(transform):
    """Concatenate a transformation onto the current transformation.

    transform must be a sequence that evaluates to 16 floating point
    values (4x4 matrix).

    Example: ConcatTransform([2,0,0,0, 0,2,0,0, 0,0,2,0, 0,0,0,1])
             ConcatTransform([[2,0,0,0], [0,2,0,0], [0,0,2,0], [0,0,0,1]])
    """

    _ribout.write('ConcatTransform '+_seq2list(transform,16)+"\n")

# Transform
def Transform(transform):
    """Set the current transformation.

    transform must be a sequence that evaluates to 16 floating point
    values (4x4 matrix).

    Example: Transform([2,0,0,0, 0,2,0,0, 0,0,2,0, 0,0,0,1])
             Transform([[2,0,0,0], [0,2,0,0], [0,0,2,0], [0,0,0,1]])
    """

    _ribout.write('Transform '+_seq2list(transform,16)+"\n")

# Sides
def Sides(nsides):
    """Specify the number of visible sides of subsequent surfaces.

    Example: Sides(1)"""

    if nsides!=1 and nsides!=2:
        _error(RIE_RANGE, RIE_ERROR, "The number of sides (nsides) must be either 1 or 2.")

    _ribout.write('Sides %s\n'%nsides)

# Orientation
def Orientation(orientation):
    """Set the orientation of subsequent surfaces.

    orientation is either OUTSIDE, INSIDE, LH (left handed)
    or RH (right handed).
    """

    _ribout.write('Orientation "'+orientation+'"\n')

# ReverseOrientation
def ReverseOrientation():
    """Causes the current orientation to be toggled.

    Example: ReverseOrientation()
    """

    _ribout.write('ReverseOrientation\n')

# Matte
def Matte(onoff):
    """Indicates whether subsequent primitives are matte objects.

    Example: Matte(TRUE)
    """
    if onoff:
        _ribout.write('Matte 1\n')
    else:
        _ribout.write('Matte 0\n')

# LightSource
def LightSource(name, *paramlist, **keyparams):
    """Add another light source and return its light handle.

    name is the name of the light source shader. You can set a user defined
    string handle via the HANDLEID parameter.

    Example: light1 = LightSource("distantlight", intensity=1.5)
    """
    global _lighthandle

    paramlist = _merge_paramlist(paramlist, keyparams)
    lshandle = None
    for i in range(0, len(paramlist), 2):
        token = paramlist[i]
        if token==HANDLEID:
            lshandle = str(paramlist[i+1])
            paramlist = paramlist[:i]+paramlist[i+2:]
            break

    # Check if the user provided a handle id...
    if lshandle is None:
        _lighthandle += 1
        lshandle = _lighthandle
        _ribout.write('LightSource "%s" %d%s\n'%(name, lshandle, _paramlist2string(paramlist, {})))
    else:
        _ribout.write('LightSource "%s" "%s"%s\n'%(name, lshandle, _paramlist2string(paramlist, {})))
        
    return lshandle

# Illuminate
def Illuminate(light, onoff):
    """Activate or deactive a light source.

    Example: Illuminate(lgt, TRUE)
    """

    if type(light)==str or type(light)==unicode:
        _ribout.write('Illuminate "%s" %d\n'%(light, onoff))
    else:
        _ribout.write('Illuminate %d %d\n'%(light, onoff))
        

# AreaLightSource
def AreaLightSource(name, *paramlist, **keyparams):
    """Start the definition of an area light and return the light handle.

    You can set a user defined string handle via the HANDLEID parameter.
    
    Example: AttributeBegin()
             area1 = AreaLightSource("arealight", intensity=0.75)
             ....
             AttributeEnd()
             Illuminate(area1, TRUE)
    """
    global _lighthandle

    # Check if the user provided a handle id...
    if HANDLEID in keyparams:
        lshandle = str(keyparams[HANDLEID])
        del keyparams[HANDLEID]
        _ribout.write('AreaLightSource "%s" "%s"%s\n'%(name, lshandle, _paramlist2string((), keyparams)))
    else:
        _lighthandle+=1
        lshandle = _lighthandle
        _ribout.write('AreaLightSource "%s" %d%s\n'%(name, lshandle, _paramlist2string((), keyparams)))

    return lshandle

# Declare
def Declare(name, declaration):
    """Declare the name and type of a variable.

    The syntax of the declaration is:  [class] [type] ['['n']']

    class ::= constant | uniform | varying | vertex
    type  ::= float | integer | string | color | point | vector | normal |
              matrix | hpoint
    
    Example: Declare("foo","uniform float")
             Declare("bar","constant integer [4]")
             Declare("mycolor", "varying color")
    """

    global _declarations

    if declaration==NULL:
        declaration=""
        
    _ribout.write('Declare "'+name+'" "'+declaration+'"\n')
    _declarations[name]=declaration
    return name

# ArchiveRecord
def ArchiveRecord(type, format, *args):
    """Output a user data record.

    type is one of COMMENT, STRUCTURE or VERBATIM.

    For comments and structural hints you can use the special variables
    $CREATOR, $DATE and $USER which will be replaced by their appropriate
    value (program name, date string, user name).

    Example: ArchiveRecord(COMMENT, "Frame %d", 2)
             ArchiveRecord(STRUCTURE, "CreationDate $DATE")
    """

    if type!=VERBATIM and format.find("$")!=-1:
        format = format.replace("$DATE", time.ctime())
        format = format.replace("$CREATOR", sys.argv[0])
        try:
            user = getpass.getuser()
        except:
            user = "<unknown>"
        format = format.replace("$USER", user)

    if type==COMMENT:
        outstr = "# "+format%args+"\n"
    elif type==STRUCTURE:
        outstr = "##"+format%args+"\n"
    elif type==VERBATIM:
        outstr = format%args
    else:
        return

    # Use the writeArchiveRecord() if there is any, otherwise use write()
    # (the latter case happens when Begin() wasn't called. _ribout is
    # then set to stdout)
    if hasattr(_ribout, "writeArchiveRecord"):
        _ribout.writeArchiveRecord(outstr)
    else:
        _ribout.write(outstr)
    
    
# ReadArchive
def ReadArchive(filename, callback=None, *ignore):
    """Include an archive file.

    In this implementation the callback function is not used and can
    be left out.

    Example: ReadArchive("teapot.rib")"""

    _ribout.write('ReadArchive "'+filename+'"\n')

# ArchiveBegin
def ArchiveBegin(archivename, *paramlist, **keyparams):
    """Begin an inline archive.
    
    Example: ArchiveBegin("myarchive")
             ...
             ArchiveEnd()
             ReadArchive("myarchive")
    """
    _ribout.write('ArchiveBegin "%s"%s\n'%(archivename, _paramlist2string((), keyparams)))
    return archivename

# ArchiveEnd
def ArchiveEnd():
    """Terminate an inline archive.
    
    Example: ArchiveBegin("myarchive")
             ...
             ArchiveEnd()
             ReadArchive("myarchive")
    """
    _ribout.write('ArchiveEnd\n')


def ProcDelayedReadArchive(): return "DelayedReadArchive"
def ProcRunProgram(): return "RunProgram"
def ProcDynamicLoad(): return "DynamicLoad"
def ProcFree(data): pass

# Procedural
def Procedural(data, bound, subdividefunc, freefunc=None):
    """Declare a procedural model.

    subdividefunc and freefunc may either be the standard RenderMan
    procedurals (ProcDelayedReadArchive, ProcRunProgram,
    ProcDynamicLoad and ProcFree) or Python callables.
    In the former case, data must be a sequence of strings or a single
    string containing the data for the functions. In the latter case,
    data may be any Python object which is just passed on to the
    functions. 
    freefunc is optional and defaults to None.

    Because this module can only produce RIB, a custom subdivide function is
    simply called with a detail value of INFINITY to generate all the
    data at once.
    
    Example: Procedural("mymodel.rib", [-1,1,-1,1,-1,1], \\
                          ProcDelayedReadArchive, NULL)
                          
             Procedural(["python teapot.py",""],[0,1,0,1,0,1], \\
                          ProcRunProgram, NULL)
                          
             Procedural(["teapot.so",""],[0,1,0,1,0,1], \\
                          ProcDynamicLoad, NULL)
    """
    if subdividefunc in [ProcDelayedReadArchive, ProcRunProgram, ProcDynamicLoad]:
        if type(data)==types.StringType:
            data=[data]
        _ribout.write('Procedural "'+subdividefunc()+'" '+_seq2list(data)+ \
                     ' '+_seq2list(bound,6)+"\n")
    else:
        # Call the custom procedure to generate all the data...
        subdividefunc(data, INFINITY)
        if freefunc is not None:
            freefunc(data)

# Geometry
def Geometry(type, *paramlist, **keyparams):
    """Create an implementation-specific geometric primitive.

    Example: Geometry("teapot")
    """

    _ribout.write('Geometry "'+type+'"'+_paramlist2string(paramlist, keyparams)+"\n")

# Bound
def Bound(bound):
    """Set the bounding box for subsequent primitives.

    bound must be a sequence of six floating point values specifying
    the extent of the box along each coordinate direction:
    bound = [xmin, xmax, ymin, ymax, zmin, zmax]

    Example: Bound([-1,1, 0,1, 0.5,0.75])
    """

    _ribout.write('Bound '+_seq2list(bound,6)+'\n')
    
# SolidBegin
def SolidBegin(type):
    """Start the definition of a solid object.

    type is one of PRIMITIVE, UNION, DIFFERENCE and INTERSECTION.

    Example: SolidBegin(INTERSECTION)
             SolidBegin(PRIMITIVE)
             ...
             SolidEnd()
             SolidBegin(PRIMITIVE)
             ...
             SolidEnd()
             SolidEnd()
    """

    _ribout.write('SolidBegin "'+type+'"\n')

# SolidEnd
def SolidEnd():
    """Terminate the definition of a solid object."""

    _ribout.write('SolidEnd\n')

# ObjectBegin
def ObjectBegin(*paramlist, **keyparams):
    """Start the definition of a retained model and return the object handle.

    You can pass a user defined string handle via the HANDLEID parameter.

    Example: obj1 = ObjectBegin()
             ...
             ObjectEnd()
    """
    global _objecthandle, _insideobject

    if _insideobject:
        _error(RIE_ILLSTATE, RIE_ERROR, "Object blocks cannot be nested.")

    keyparams = _paramlist2dict(paramlist, keyparams)

    # Check if the user provided a handle id...
    if HANDLEID in keyparams:
        # objhandle = str(keyparams[HANDLEID])
        objhandle = keyparams[HANDLEID]
        del keyparams[HANDLEID]
        if type(objhandle) == str or type(objhandle)==unicode:
            _ribout.write('ObjectBegin "%s"\n'%objhandle)
        else:
            _ribout.write('ObjectBegin %d\n'%objhandle)
    else:
        _objecthandle+=1
        objhandle = _objecthandle
        _ribout.write('ObjectBegin %d\n'%objhandle)
    
    _insideobject=1

    return objhandle

# ObjectEct
def ObjectEnd():
    """Terminate the definition of a retained model."""

    global _insideobject
    
    _ribout.write('ObjectEnd\n')
    _insideobject=0

# ObjectInstance
def ObjectInstance(handle):
    """Create an instance of a previously defined model.

    Example: ObjectInstance(obj1)
    """

    if type(handle)==str or type(handle)==unicode:
        _ribout.write('ObjectInstance "%s"\n'%handle)
    else:
        _ribout.write('ObjectInstance %d\n'%handle)

# TextureCoordinates
def TextureCoordinates(s1, t1, s2, t2, s3, t3, s4, t4):
    """Set the current set of texture coordinates.

    Declares a projection from the unit square [(0,0), (1,0), (0,1), (1,1)]
    in parameter space to quadrilateral [(s1,t1), (s2,t2), (s3,t3), (s4,t4)]
    in texture space.

    Example: TextureCoordinates(0.0, 0.0, 2.0, -0.5, -0.5, 1.75, 3.0, 3.0)"""

    _ribout.write('TextureCoordinates %s %s %s %s %s %s %s %s\n'%(s1,t1,s2,t2,s3,t3,s4,t4))

# MakeTexture
def MakeTexture(picname, texname, swrap, twrap, filterfunc, swidth, twidth, *paramlist, **keyparams):
    """Convert an image file into a texture file.

    swrap and twrap are one of PERIODIC, CLAMP or BLACK.
    filterfunc has to be one of the predefined filter functions:
    GaussianFilter, BoxFilter, TriangleFilter, SincFilter or
    CatmullRomFilter (otherwise a warning is issued and the call is ignored).
    swidth and twidth define the support of the filter.

    Example: MakeTexture("img.tif", "tex.tif", PERIODIC, CLAMP, \\
                           GaussianFilter, 2,2)
    """
    
    if callable(filterfunc):
        _error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
        return

    _ribout.write('MakeTexture "'+picname+'" "'+texname+'" "'+swrap+'" "'+
                  twrap+'" "'+filterfunc+'" '+str(swidth)+' '+str(twidth)+
                  _paramlist2string(paramlist, keyparams)+'\n')

# MakeLatLongEnvironment
def MakeLatLongEnvironment(picname, texname, filterfunc, swidth, twidth, *paramlist, **keyparams):
    """Convert an image file into an environment map.

    filterfunc has to be one of the predefined filter functions:
    GaussianFilter, BoxFilter, TriangleFilter, SincFilter or
    CatmullRomFilter (otherwise a warning is issued and the call is ignored).
    swidth and twidth define the support of the filter.

    Example: MakeLatLongEnvironment("img.tif", "tex.tif",
                                      GaussianFilter, 2,2)
    """
    
    if callable(filterfunc):
        _error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
        return

    _ribout.write('MakeLatLongEnvironment "'+picname+'" "'+texname+'" "'+
                  filterfunc+'" '+str(swidth)+' '+str(twidth)+
                  _paramlist2string(paramlist, keyparams)+'\n')

# MakeCubeFaceEnvironment
def MakeCubeFaceEnvironment(px,nx,py,ny,pz,nz, texname, fov, filterfunc, swidth, twidth, *paramlist, **keyparams):
    """Convert six image files into an environment map.

    The px/nx images are the views in positive/negative x direction.
    fov is the field of view that was used to generate the individual images.
    filterfunc has to be one of the predefined filter functions:
    GaussianFilter, BoxFilter, TriangleFilter, SincFilter or
    CatmullRomFilter (otherwise a warning is issued and the call is ignored).
    swidth and twidth define the support of the filter.

    Example: MakeCubeFaceEnvironment("px.tif","nx.tif","py.tif","ny.tif",
                                       "pz.tif","nz.tif", "tex.tif", 92.0,
                                        GaussianFilter, 2,2)
    """
    
    if callable(filterfunc):
        _error(RIE_INCAPABLE, RIE_WARNING, "Only the standard filters can be stored in a RIB stream.")
        return

    _ribout.write('MakeCubeFaceEnvironment "'+px+'" "'+nx+'" "'+
                  py+'" "'+ny+'" "'+pz+'" "'+nz+'" "'+ texname+'" '+
                  str(fov)+' "'+filterfunc+'" '+str(swidth)+' '+str(twidth)+
                  _paramlist2string(paramlist, keyparams)+'\n')

# MakeShadow
def MakeShadow(picname, shadowname, *paramlist, **keyparams):
    """Transform a depth image into a shadow map.

    Example: MakeShadow("depthimg.tif", "shadow.tif")
    """
    
    _ribout.write('MakeShadow "'+picname+'" "'+shadowname+'"'+_paramlist2string(paramlist, keyparams)+'\n')

# MakeBrickMap
def MakeBrickMap(ptcnames, bkmname, *paramlist, **keyparams):
    """Create a brick map file from a list of point cloud file names.

    Example: MakeBrickMap(["sphere.ptc", "box.ptc"], "spherebox.bkm", "float maxerror", 0.002)
    """
    names = " ".join(map(lambda name: '"%s"'%name, ptcnames))
    _ribout.write('MakeBrickMap [%s] "%s"%s\n'%(names, bkmname, _paramlist2string(paramlist, keyparams)))

# Detail
def Detail(bound):
    """Set the current bounding box.

    bound must be a sequence of six floating point values specifying
    the extent of the box along each coordinate direction:
    bound = [xmin, xmax, ymin, ymax, zmin, zmax]

    Example: Detail([10,20,40,70,0,1])
    """

    _ribout.write('Detail '+_seq2list(bound,6)+'\n')

# RelativeDetail
def RelativeDetail(relativedetail):
    """Set the factor for all level of detail calculations.

    Example: RelativeDetail(0.7)"""

    _ribout.write('RelativeDetail %s\n'%relativedetail)

# DetailRange
def DetailRange(minvisible, lowertransition, uppertransition, maxvisible):
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

    Example: DetailRange(0,0,10,20)
    """

    _ribout.write('DetailRange %s %s %s %s\n'%(minvisible, lowertransition, uppertransition, maxvisible))

# CoordinateSystem
def CoordinateSystem(spacename):
    """Mark the current coordinate system with a name.

    Example: CoordinateSystem("lamptop")
    """
    _ribout.write('CoordinateSystem "'+spacename+'"\n')

# ScopedCoordinateSystem
def ScopedCoordinateSystem(spacename):
    """Mark the current coordinate system with a name but store it on a separate stack.

    Example: ScopedCoordinateSystem("lamptop")
    """
    _ribout.write('ScopedCoordinateSystem "'+spacename+'"\n')

# TransformPoints
def TransformPoints(fromspace, tospace, points):
    """Transform a set of points from one space to another.

    This function is not implemented and always returns None.
    """

    return None

# CoordSysTransform
def CoordSysTransform(spacename):
    """Replace the current transformation matrix with spacename.

    Example: CoordSysTransform("lamptop")
    """

    _ribout.write('CoordSysTransform "'+spacename+'"\n')

# Context
def Context(handle):
    """Set the current active rendering context.

    Example: ctx1 = GetContext()
             ...
             Context(ctx1)
    """

    _switch_context(handle)

# GetContext
def GetContext():
    """Get a handle for the current active rendering context.

    Example: ctx1 = GetContext()
             ...
             Context(ctx1)"""

    global _current_context

    return _current_context

# System
def System(cmd):
    """Execute an arbitrary command in the same environment as the current rendering pass.
    """
    # Escape quotes
    cmd = cmd.replace('"', r'\"')
    _ribout.write('System "%s"\n'%cmd)

# IfBegin
def IfBegin(expression, *paramlist, **keyparams):
    """Begin a conditional block.
    """
    _ribout.write('IfBegin "%s"%s\n'%(expression, _paramlist2string(paramlist, keyparams)))

# ElseIf
def ElseIf(expression, *paramlist, **keyparams):
    """Add an else-if block to a conditional block.
    """
    
    _ribout.write('ElseIf "%s"%s\n'%(expression, _paramlist2string(paramlist, keyparams)))

# Else
def Else():
    """Add an else block to a conditional block.
    """
    
    _ribout.write('Else\n')

# IfEnd
def IfEnd():
    """Terminate a conditional block.
    """
    
    _ribout.write('IfEnd\n')
    
# Resource
def Resource(handle, type, *paramlist, **keyparams):
    """Create or operate on a named resource of a particular type.
    """
    _ribout.write('Resource "%s" "%s"%s\n'%(handle, type, _paramlist2string(paramlist, keyparams)))

# ResourceBegin
def ResourceBegin():
    """Push the current set of resources. 
    """
    _ribout.write('ResourceBegin\n')

# ResourceEnd
def ResourceEnd():
    """Pop the current set of resources. 
    """
    _ribout.write('ResourceEnd\n')

##################### Global variabels (internal) ####################

_contexts     = {}
_current_context = None

####

# Initially the output stream is stdout (and not an instance of RIBStream)
# In interactive sessions this prevents the version number to be written.
_ribout       = sys.stdout
_colorsamples = 3
_lighthandle  = 0
_objecthandle = 0
_errorhandler = ErrorPrint
_declarations = {}

_insideframe  = 0
_insideworld  = 0
_insideobject = 0
_insidesolid  = 0
_insidemotion = 0

# If you're adding new global variables then make sure that they're
# saved and loaded from the context handling functions and initialized
# in Begin() and during the module initialization.

##################### Internal helper functions #######################

def _save_context(handle):
    "Save a context."
    ctx = (_ribout, _colorsamples, _lighthandle, _objecthandle,
           _errorhandler, _declarations,
           _insideframe, _insideworld, _insideobject, _insidesolid,
           _insidemotion)
    _contexts[handle]=ctx

def _load_context(handle):
    "Load a context."
    global _ribout, _colorsamples, _lighthandle, _objecthandle
    global _errorhandler, _declarations, _insideframe, _insideworld
    global _insideobject, _insidesolid, _insidemotion

    _ribout, _colorsamples, _lighthandle, _objecthandle, \
    _errorhandler, _declarations, \
    _insideframe, _insideworld, _insideobject, _insidesolid, \
    _insidemotion = _contexts[handle]

def _create_new_context():
    "Create a new context and make it the active one."
    global _current_context

    keys = _contexts.keys()
    if len(keys)>0:
        handle = max(keys)+1
    else:
        handle = 1
    _contexts[handle]=()
    
    if _current_context!=None:
        _save_context(_current_context)

    _current_context = handle

def _switch_context(handle):
    "Save the current context and make another context the active one."
    global _current_context
    
    if _current_context!=None:
        _save_context(_current_context)
    _current_context = handle
    _load_context(handle)

def _destroy_context():
    "Destroy the current active context"
    global _contexts, _current_context

    handle = _current_context
    del _contexts[handle]
    _current_context = None

def _init_declarations():
    global _declarations
    _declarations = {P:"vertex point", PZ:"vertex point",
                     PW:"vertex hpoint",
                     N:"varying normal", NP:"uniform normal",
                     CS:"varying color", OS:"varying color",
                     S:"varying float", T:"varying float",
                     ST:"varying float[2]",
                     ORIGIN:"integer[2]",
                     KA:"uniform float",
                     KD:"uniform float",
                     KS:"uniform float",
                     ROUGHNESS:"uniform float",
                     KR:"uniform float",
                     TEXTURENAME:"string",
                     SPECULARCOLOR:"uniform color",
                     INTENSITY:"float",
                     LIGHTCOLOR:"color",
                     FROM:"point",
                     TO:"point",
                     CONEANGLE:"float",
                     CONEDELTAANGLE:"float",
                     BEAMDISTRIBUTION:"float",
                     AMPLITUDE:"uniform float",
                     MINDISTANCE:"float",
                     MAXDISTANCE:"float",
                     BACKGROUND:"color",
                     DISTANCE:"float",
                     FOV:"float",
                     WIDTH:"varying float",
                     CONSTANTWIDTH:"constant float",
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

def _error(code, severity, message):
    global _errorhandler, LastError

    LastError = code

    st = inspect.stack(1)
    # Search the offending  function in the stack...
    j=None
    for i in range(len(st)):
        if st[i][3][:2]=="":
            j=i
    # No function beginning with "" found? That's weird. Maybe someone
    # messed with the function names.
    if j==None:
        where=""
    else:
        # name of the  function
        call   = inspect.stack(0)[j][3]
        # filename and line number where the offending  call occured
        file   = inspect.stack(1)[j+1][1]
        line   = inspect.stack(1)[j+1][2]
        if file==None: file="?"
        where = 'In file "'+file+'", line '+`line`+' - '+call+"():\n"

    _errorhandler(code,severity,where+message)

def _seq2col(seq):
    """Convert a sequence containing a color into a string."""
    if len(seq)<_colorsamples:
        _error(RIE_INVALIDSEQLEN, RIE_ERROR, "Invalid sequence length ("+\
               `len(seq)`+" instead of "+`_colorsamples`+")")
    colseq = tuple(seq)
    return '['+string.join( map(lambda x: str(x), colseq[:_colorsamples]) )+']'

def _flatten(seq):
    """Return a list of the individual items in a (possibly nested) sequence.

    Returns a list with all items as strings.
    If an item was already a string it's enclosed in apostrophes.
    
    Example: _flatten( [(1,2,3), (4,5,6)] ) -> ["1","2","3","4","5","6"]
             _flatten( ("str1","str2") )    -> ['"str1"','"str2"']
    """
    res = []
    ScalarTypes = [types.IntType, types.LongType, types.FloatType]
    for v in seq:
        vtype = type(v)
        # v=scalar?
        if vtype in ScalarTypes:
            res.append(str(v))
        # vec3?
        #elif isinstance(v, _vec3):
            #res.extend([str(v.x), str(v.y), str(v.z)])
        # v=string?
        elif isinstance(v, basestring):
            res.append('"%s"'%v)
        # no scalar or string. Then it might be a sequence...
        else:
            # Check if it is really a sequence...
            try:
                n = len(v)
            except:
                res.append(str(v))
                continue
            res += _flatten(v)
    return res

def _seq2list(seq, count=None):
    """Convert a sequence into a string.

    The function checks if the sequence contains count elements (unless
    count is None). If it doesn't an error is generated.
    The return value is a string containing the sequence. The string can
    be used as parameter value to RIB commands.
    """

    f = _flatten(seq)
    # Has the sequence an incorrect length? then generate an error
    if count!=None and len(f)!=count:
        _error(RIE_INVALIDSEQLEN, RIE_ERROR, "Invalid sequence length ("+\
               `len(f)`+" instead of "+`count`+")")
        
    return '[%s]'%" ".join(f)

def _paramlist2dict(paramlist, keyparams):
    """Combine the paramlists (tuple & dict) into one dict.
    
    paramlist is a tuple with function arguments (token/value pairs or
    a dictionary). keyparams is a dictionary with keyword arguments.
    The dictionary keyparams will be modified and returned.
    """

    if len(paramlist)==1 and type(paramlist[0])==types.DictType:
        keyparams = paramlist[0]
        paramlist = ()
    
    # Add the paramlist tuple to the keyword argument dict
    for i in range(len(paramlist)/2):
        token = paramlist[i*2]
        value = paramlist[i*2+1]
        keyparams[token]=value

    return keyparams

def _paramlist2lut(paramlist, keyparams):
    """Combine the paramlists into one dict without inline declarations.

    paramlist is a tuple with function arguments. keyparams is a
    dictionary with keyword arguments. The dictionary keyparams will
    be modified and returned.

    The resulting dictionary can be used to look up the value of tokens.
    """
    # Add the paramlist tuple to the keyword argument dict
    for i in range(len(paramlist)/2):
        token = paramlist[i*2]
        value = paramlist[i*2+1]
        # Extract the name of the token (without inline declaration
        # if there is one)
        f = token.split(" ")
        tokname = f[-1]
        keyparams[tokname]=value

    return keyparams
    
def _merge_paramlist(paramlist, keyparams):
    """Merge a paramlist tuple and keyparams dict into one single list.
    """
    if len(paramlist)==1 and type(paramlist[0])==types.DictType:
        keyparams = paramlist[0]
        paramlist = ()

    res = list(paramlist)
    # Check if the number of values is uneven (this is only allowed when
    # the last value is None (NULL) in which case this last value is ignored)
    if (len(res)%2==1):
       if res[-1] is None:
           res = res[:-1]
       else:
           raise ValueError, "The parameter list must contain an even number of values" 

    # Append the params from the keyparams dict to the parameter list
    map(lambda param: res.extend(param), keyparams.iteritems())
    return res
    

def _paramlist2string(paramlist, keyparams={}):
    """Convert the paramlist into a string representation.

    paramlist is a tuple with function arguments (token/value pairs or
    a dictionary). keyparams is a dictionary with keyword arguments.
    Each token has to be a string, the value can be of any type. If the
    value is a string, it's enclosed in apostrophes. A trailing token
    without a value is ignored, which also means that a trailing NULL
    can be passed.
    The resulting string contains a leading space, unless there are no
    token/value pairs.
    """

    global _declarations

    paramlist = _merge_paramlist(paramlist, keyparams)


    res=""
    for i in range(0, len(paramlist), 2):
        token = paramlist[i].strip()
        value = paramlist[i+1]
        # Extract the name of the token (without inline declaration
        # if there is one)
        f = token.split(" ")
        tokname = f[-1:][0]
        inline  = f[:-1]

        if not (_declarations.has_key(tokname) or inline!=[]):
            _error(RIE_UNDECLARED,RIE_ERROR,'Parameter "'+tokname+
                   '" is not declared.')
        
        # Check if the value is a sequence (if it returns an iterator)
        isseq=0
        try:
            isseq = (iter(value)!=None)
        except:
            pass
        # Convert value into the appropriate string representation
        if isinstance(value, basestring):
            value='["'+value+'"]'
#        elif type(value)==types.ListType or type(value)==types.TupleType:
        elif isseq:
            value = _seq2list(value)
        else:
            value='[%s]'%value
        res+=' "'+token+'" '+value

    if (res==" "): res=""
    return res


############################################################

_init_declarations()
