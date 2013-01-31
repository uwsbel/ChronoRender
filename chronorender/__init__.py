import sys, os, inspect

# get submodule paths
currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])

# do select paths
# submodpaths = [                 \
               # 'datareader',    \
               # 'geometry',      \
               # 'lighting',      \
               # 'renderobject',  \
               # 'renderpass',    \
               # 'rendersettings',\
               # 'scene',         \
               # 'shader',        \
               # 'simulation',    \
               # 'visualizer'     \
               # ]
# paths = [currpath]
# for path in submodpaths:
    # paths.append(os.path.join(currpath, path))

# do all
paths = [currpath]
# for entry in os.listdir(currpath):
    # if os.path.isdir(entry):
        # paths.append(os.path.abspath(entry))

for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# import finder
# import metadata
# import rndr_job
# import rndr_doc
# import cr
# import ri
# from rndr_job import *
# from rndr_doc import *
# from cr import *
