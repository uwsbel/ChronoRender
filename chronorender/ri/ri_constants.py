########################### Constants #############################

RI_NULL         = None

RI_TRUE         = 1
RI_FALSE        = 0

RI_HIDDEN       = "hidden"
RI_PAINT        = "paint"

RI_EPSILON      = 1.0e-10
RI_INFINITY     = 1.0e38

RI_FILE         = "file"
RI_FRAMEBUFFER  = "framebuffer"
RI_RGB          = "rgb"
RI_RGBA         = "rgba"
RI_RGBZ         = "rgbZ"
RI_RGBAZ        = "rgbaz"
RI_A            = "a"
RI_Z            = "z"
RI_AZ           = "az"

RI_ORIGIN       = "origin"

RI_PERSPECTIVE  = "perspective"
RI_ORTHOGRAPHIC = "orthographic"
RI_FOV          = "fov"

RI_LH           = "lh"
RI_RH           = "rh"
RI_INSIDE       = "inside"
RI_OUTSIDE      = "outside"

RI_BILINEAR     = "bilinear"
RI_BICUBIC      = "bicubic"

RI_LINEAR       = "linear"
RI_CUBIC        = "cubic"

RI_CONSTANT     = "constant"
RI_SMOOTH       = "smooth"

RI_P            = "P"
RI_PW           = "Pw"
RI_PZ           = "Pz"
RI_N            = "N"
RI_NP           = "Np"
RI_NG           = "Ng"
RI_CI           = "Ci"
RI_OI           = "Oi"
RI_CS           = "Cs"
RI_OS           = "Os"
RI_S            = "s"
RI_T            = "t"
RI_ST           = "st"

RI_COMMENT      = "comment"
RI_STRUCTURE    = "structure"
RI_VERBATIM     = "verbatim"

RI_HERMITESTEP    = 2
RI_CATMULLROMSTEP = 1
RI_BEZIERSTEP     = 3
RI_BSPLINESTEP    = 1
RI_POWERSTEP      = 4

RI_PERIODIC     = "periodic"
RI_NONPERIODIC  = "nonperiodic"
RI_CLAMP        = "clamp"
RI_BLACK        = "black"

RI_FLATNESS     = "flatness"

RI_PRIMITIVE    = "primitive"
RI_UNION        = "union"
RI_DIFFERENCE   = "difference"
RI_INTERSECTION = "intersection"

RI_WIDTH        = "width"
RI_CONSTANTWIDTH = "constantwidth"

RI_HOLE         = "hole"
RI_CREASE       = "crease"
RI_CORNER       = "corner"
RI_INTERPOLATEBOUNDARY = "interpolateboundary"

RI_AMBIENTLIGHT = "ambientlight"
RI_POINTLIGHT   = "pointlight"
RI_DISTANTLIGHT = "distantlight"
RI_SPOTLIGHT    = "spotlight"

RI_INTENSITY    = "intensity"
RI_LIGHTCOLOR   = "lightcolor"
RI_FROM         = "from"
RI_TO           = "to"
RI_CONEANGLE    = "coneangle"
RI_CONEDELTAANGLE = "conedeltaangle"
RI_BEAMDISTRIBUTION = "beamdistribution"

RI_MATTE        = "matte"
RI_METAL        = "metal"
RI_SHINYMETAL   = "shinymetal"
RI_PLASTIC      = "plastic"
RI_PAINTEDPLASTIC = "paintedplastic"

RI_KA           = "Ka"
RI_KD           = "Kd"
RI_KS           = "Ks"
RI_ROUGHNESS    = "roughness"
RI_KR           = "Kr"
RI_TEXTURENAME  = "texturename"
RI_SPECULARCOLOR = "specularcolor"

RI_DEPTHCUE     = "depthcue"
RI_FOG          = "fog"
RI_BUMPY        = "bumpy"

RI_MINDISTANCE  = "mindistance"
RI_MAXDISTANCE  = "maxdistance"
RI_BACKGROUND   = "background"
RI_DISTANCE     = "distance"
RI_AMPLITUDE    = "amplitude"

RI_RASTER       = "raster"
RI_SCREEN       = "screen"
RI_CAMERA       = "camera"
RI_WORLD        = "world"
RI_OBJECT       = "object"

RI_IDENTIFIER   = "identifier"
RI_NAME         = "name"
RI_SHADINGGROUP = "shadinggroup"

RI_IGNORE       = "ignore"
RI_PRINT        = "print"
RI_ABORT        = "abort"
RI_HANDLER      = "handler"

RI_HANDLEID     = "__handleid"

# Tokens specific to the cgkit binding...
RI_RIBOUTPUT    = "_riboutput"
RI_VERSION      = "_version"

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

RiLastError     = 0

