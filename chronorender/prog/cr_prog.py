#!/usr/bin/env python
import os, imp, __main__, inspect, sys

class Prog(object):
    def __init__(self):
          self.args = self.getArgs()
          self.path , self.name = self.getPathAndName(__file__)
          self.call = self.getProgCall()

    def getArgs():
        return {}

    def parseArgs():
        self.args = {}

    def main():
        exit()

    def printErrorAndExit(self, msg):
        print "ERROR:", msg
        exit()

    def getPathAndName(self, frame):
        path, name = os.path.split(os.path.abspath(frame))
        name = self._removePYCExt(name)
        return path, name

    def getProgCall(self):
        out = self.name + " "
        for k, v in self.args.iteritems():
            if not v:
                continue
            out += "--" + k + " " + str(v) + " "
        return out

    def _removePYCExt(self, name):
        name, ext = os.path.splitext(name)
        if ext == ".pyc":
            name += ".py"
        else:
            name += ext
        return name

    def verifyMetaData(self):
        if not self.args['metadata']:
            self.printErrorAndExit('no metadata specified')
        if not os.path.exists(self.args['metadata']):
            self.printErrorAndExit('metadata does not exist: ' + str(self.args['metadata']))
        return self.args['metadata']

    @staticmethod
    def getCRBinPath():
        path = os.path.abspath(os.path.split(__main__.__file__)[1])

        currdir = path
        parentdir, basename = os.path.split(currdir)
        while basename != "chronorender" and currdir != parentdir:
            currdir = parentdir
            parentdir, basename = os.path.split(currdir)

        return os.path.join(parentdir, "bin")

# def getRenderProg():
    # binpath = getCRBinPath()

    # execn = 'crender.py'
    # execp = os.path.join(binpath, execn)
    # if not os.path.exists(execp):
        # raise Exception('could not find render prog ' + execp)

    # mod = None
    # try:
        # mod = imp.load_source(execn, binpath)
    # except:
        # raise Exception('could not import ' + execp)


    # mems = inspect.getmembers(mod)
    # for mem in mems:
        # print mem
        # if inspect.isfunction(mem):
            # print mem

    # prog = Prog()
    # prog.path = binpath
    # prog.name = execn
    # prog.call = prog.name + " render "

    # prog.args = mod.getArgs()

    # return prog

# def is_mod_function(mod, func):
      # return inspect.isfunction(func) and inspect.getmodule(func) == mod

# def list_functions(mod):
      # return [func.__name__ for func in mod.__dict__.itervalues() 
                      # if is_mod_function(mod, func)]

# TODO method to go up parent dirs
def addCRToPath():
    currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
    currpath = os.path.split(currpath)[0]
    currpath = os.path.split(currpath)[0]

    if currpath not in sys.path:
        sys.path.insert(0, currpath)

addCRToPath()

if __name__ == '__main__':
    p = Prog()
    p.main()
