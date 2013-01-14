import sys, os, inspect

# get submodule paths
currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
geopath = os.path.join(currpath, 'geometry')
robjpath = os.path.join(currpath, 'renderobject')
rpasspath = os.path.join(currpath, 'renderpass')
settingspath = os.path.join(currpath, 'rendersettings')
shaderpath = os.path.join(currpath, 'shader')

paths = [currpath, geopath, robjpath, rpasspath, settingspath, shaderpath]
for path in paths:
    if path not in sys.path:
        sys.path.insert(0, path)

from data_processor import *
from main import *
from meta_data import *
from rndr_doc import *
from ri_stream import *
import cri_stream
from finder import *
from cr import *
from rndr_job import *

# subdirs
from geometry import *
from renderobject import *
from renderpass import *
from rendersettings import *
from shader import *
# import data_processor
# import rndr_pass
# import meta_data     
# import rndr_object     
# import shader     
