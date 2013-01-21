import re, inspect, os

def natural_sort(slist):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(slist, key = alphanum_key)

def getAbsPathRelativeToModule(cls, path):
    modpath = os.path.split(inspect.getfile(cls))[0]
    return getAbsPathRelativeTo(path, modpath)

def getAbsPathRelativeTo(path, relative):
    prevdir = os.getcwd()
    os.chdir(relative)
    abspath = os.path.abspath(path)
    os.chdir(prevdir)
    return abspath
