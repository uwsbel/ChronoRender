import re, inspect, os, sys

def natural_sort(slist):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(slist, key = alphanum_key)

def getAbsPathRelativeToModule(cls, path):
    modpath = os.path.split(inspect.getfile(cls))[0]
    return getAbsPathRelativeTo(path, modpath)

def getAbsPathRelativeTo(path, relative):
    if not os.path.isdir(relative):
        relative = os.path.split(relative)[0]

    prevdir = os.getcwd()
    os.chdir(relative)
    abspath = os.path.abspath(path)
    os.chdir(prevdir)
    return abspath

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def findModuleOnSysPath(module, path=None):
    if path:
        out = findFileOnPath(module, path)
        if out:
          out = os.path.split(out)[1]
          out = os.path.splitext(out)[0]
        return out

    for p in sys.path:
        out = findFileOnPath(module, p)
        if out: return out

    return None

def findFileOnPath(fname, path):
    for root, dirs, files in os.walk(path):
        if fname in files:
            return os.path.join(root,fname)
    return None

def getCRAssetPaths():
    paths = []
    cr_path = os.path.split(inspect.getfile(inspect.currentframe()))[0]
    a_path = os.path.join(cr_path, 'assets')
    for root, dirs, files in os.walk(a_path):
        paths.append(root)
    return paths
