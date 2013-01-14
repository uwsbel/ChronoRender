import sys, os, inspect

# get submodule paths
currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
submodpaths = [                 \
               'datareader',    \
               'geometry',      \
               'lighting',      \
               'renderobject',  \
               'renderpass',    \
               'rendersettings',\
               'scene',         \
               'shader',        \
               'simulation',    \
               'visualizer'     \
               ]

paths = [currpath]
for path in submodpaths:
    paths.append(os.path.join(currpath, path))

for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

from data_processor import *
from main import *
from meta_data import *
from rndr_doc import *
from ri_stream import *
from cr import *
import cri_stream
from finder import *
from rndr_job import *

# subdirs
from datareader import *
from geometry import *
from lighting import *
from renderobject import *
from renderpass import *
from rendersettings import *
from scene import *
from shader import *
from simulation import *
from visualizer import *

