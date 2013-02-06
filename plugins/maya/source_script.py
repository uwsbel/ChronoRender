import sys
import os
 
def psource(module):
 
    file = os.path.basename( module )
    dir = os.path.dirname( module )
 
    toks = file.split( '.' )
    modname = toks[0]
 
    # Check if dirrectory is really a directory
    if( os.path.exists( dir ) ):
 
    # Check if the file directory already exists in the sys.path array
        paths = sys.path
        pathfound = 0
        for path in paths:
            if(dir == path):
                pathfound = 1
 
    # If the dirrectory is not part of sys.path add it
        if not pathfound:
            sys.path.append( dir )
 
    # exec works like MEL's eval but you need to add in globals() 
    # at the end to make sure the file is imported into the global 
    # namespace else it will only be in the scope of this function
    exec ('import ' + modname) in globals()
 
    # reload the file to make sure its up to date
    exec( 'reload( ' + modname + ' )' ) in globals()
 
    # This returns the namespace of the file imported
    return modname
 
# When you import a file you must give it the full path
psource( 'Z:\\VM_Shader\\Arch_Shader\\gorb.py' )

gorb.main()