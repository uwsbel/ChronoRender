import sys, os, inspect

def addCRToPath():
    currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
    currpath = os.path.split(currpath)[0]

    if currpath not in sys.path:
        sys.path.insert(0, currpath)
