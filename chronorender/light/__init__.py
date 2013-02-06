import sys, os, inspect

# get submodule paths
currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
paths = [currpath]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

from cr import ChronoRender
