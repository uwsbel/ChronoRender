import sys, os, os.path
import ctypes.util
from chronorender.cr_utils import which

_supported = { 
        'aqsis' : {'lib' : 'aqsis_core', 
                   'shader' : 'aqsl', 
                   'texture' : 'teqser'},

        'pixie' : {'lib' : 'ri', 
                   'shader' : 'sdr', 
                   'texture' : 'texmake'},

        '3delight' : {'lib' : '3delight', 
                   'shader' : '', 
                   'texture' : ''},

        'prman' : {'lib' : 'prman', 
                   'shader' : 'shader', 
                   'texture' : 'txmake'},

        'stdout' : {'lib' : None, 
                   'shader' : None, 
                   'texture' : None}
        }

def resolveRManLib(libName, renderer=None):
    """Resolve the given library name.

    If the name is an absolute file name, it is just returned unmodified.
    Otherwise the method tries to resolve the name and return an absolute
    path to the library. If no library file could be found, the name
    is returned unmodified.
    
    renderer may be the name of a renderer package (aqsis, pixie, 3delight,
    prman) which serves as a hint to which package the library belongs to.
    If not given, the renderer is determined from the library name.
    """
    if os.path.isabs(libName):
        return libName
    
    # Try to figure out the location of the lib
    lib = ctypes.util.find_library(libName)
    if lib is not None:
        return lib

    # A list of library search paths...
    searchPaths = []

    # Is there a renderer-specific search path?
    if renderer is None:
        renderer = rendererFromLib(libName)
    libDir = rendererLibDir(renderer)
    if libDir is not None:
        searchPaths.append(libDir)

    # Also examine LD_LIBRARY_PATH if we are on Linux
    if sys.platform.startswith("linux"):
        libPaths = os.getenv("LD_LIBRARY_PATH")
        if libPaths is not None:
            searchPaths.extend(libPaths.split(":"))

    # Check the search paths...
    libFileName = libraryFileName(libName)
    for path in searchPaths:
        lib = os.path.join(path, libFileName)
        if os.path.exists(lib):
            return lib

    # Nothing found, then just return the original name
    return libName

def resolveRManShdrc(renderer):
    shdrc = sdrcFromRenderer(renderer)
    return which(sdrc)

def sdrcFromRenderer(name):
    if rendererSupported(name):
        return _supported[name]['shader']

def txmkFromRenderer(name):
    if rendererSupported(name):
        return _supported[name]['texture']

def libFromRenderer(name):
    if rendererSupported(name):
        return _supported[name]['lib']

def rendererSupported(name):
    if name not in _supported:
        raise Exception('renderer: ' + str(name) + ' not supported')
    return True

def rendererFromLib(libName):
    """Return the renderer package name given a library name.
    
    libName is the name of a RenderMan library. The function tries to
    determine from which renderer it is and returns the name of the
    render package. None is returned if the library name is unknown.
    """
    name = os.path.basename(libName)
    name = os.path.splitext(name)[0]
    if name.startswith("lib"):
        name = name[3:]
        
    if name in ["aqsislib", "ri2rib", "slxargs"]:
        return "aqsis"
    elif libName in ["sdr", "ri"]:
        return "pixie"
    elif libName in ["3delight"]:
        return "3delight"
    elif libName in ["prman"]:
        return "prman"
    
    return None

def rendererLibDir(renderer):
    """Return a renderer-specific library path.
    
    The return path is based on a renderer-specific environment variable.
    None is returned when no path could be determined.
    renderer may be None, "aqsis", "pixie", "3delight" or "prman" (case-insensitive).
    """
    if renderer is None:
        return None
    
    envVarDict = {"aqsis":"AQSISHOME",
                  "pixie":"PIXIEHOME",
                  "3delight":"DELIGHT",
                  "prman":"RMANTREE"}
    
    envVar = envVarDict.get(renderer.lower())
    if envVar is not None:
        base = os.getenv(envVar)
        if base is not None:
            return os.path.join(base, "lib")
    return None

def libraryFileName(libName):
    """Extend a base library name to a file name.

    Example:  "foo" -> "libfoo.so"    (Linux)
                    -> "foo.dll"      (Windows)
                    -> "libfoo.dylib" (OSX)
    """
    if sys.platform.startswith("linux"):
        return "lib%s.so"%libName
    elif sys.platform=="darwin":
        return "lib%s.dylib"%libName
    elif sys.platform.startswith("win"):
        return "%s.dll"%libName
    return libName

#####################################################################
if __name__=='__main__':
    pass
