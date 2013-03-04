#!/usr/bin/env python

# import argparse, os
import script_utils as su
su.addCRToPath()

# from chronorender.cr import ChronoRender
import sys, subprocess, inspect, os
import chronorender.prog as prog


def main():
    # args = getArgs()
    if len(sys.argv) < 2:
        printHelpAndExit()

    action = sys.argv[1]
    if action not in getOptions():
        printHelpAndExit()

    args = sys.argv[2:len(sys.argv)]
    exe = None
    if action == 'init':
        exe = prog.CRenderInit()
    elif action == 'render':
        exe = prog.CRenderLocal()
    elif action == 'submit':
        exe = prog.CRenderDist()
    elif action == 'update':
        exe = prog.CRenderUpdate()
    args.insert(0, getExecName(exe))
    args.insert(0, 'python')
    print "ARGS", args
    subprocess.call(args)
        # updateJobAssets(args)

def getOptions():
    return ['init', 'update', 'render', 'submit']

def getHelpMsg():
    out = "crender usage:\n"
    out += "crender " + str(getOptions())
    return out

def getExecName(exe):
    path = inspect.getfile(type(exe))
    # name, ext = os.path.splitext(os.path.split(path)[1])
    name, ext = os.path.splitext(path)
    # if ext == ".pyc":
        # ext = ".py"
    return name + ext

def printHelpAndExit():
    print getHelpMsg()
    exit()

# def getArgs():
    # parser.add_argument('-m', '--metadata', help='the data file that contains the \
            # render job info', required=False)

    # parser.add_argument('-r', '--renderer', 
            # help='which renderer to use, dumps to stdout by default', 
            # default='stdout',
            # required=False)

    # parser.add_argument('-o', '--outpath', help='used with init, where to \
            # generate the render files; cwd if not set', required=False)

    # parser.add_argument('-j', '--jobmanager', 
            # choices=['torque'],
            # help='specify the distrbuted job manager you are using; default=torque', 
            # required=False)

    # parser.add_argument('-f', '--framerange',
            # nargs=2,
            # help='render the specified framerange; by default renders all frames',
            # default=None,
            # type=int,
            # required=False)
    # return vars(parser.parse_args())

# def initNewRenderJob(args):
    # path = args['outpath'] if args['outpath'] else os.getcwd()

    # cr = ChronoRender()
    # cr.generateRenderJobToDisk(path)

# def startLocalRenderJob(args):
    # md = verifyMetadata(args)
    # stream = args['renderer']
    # frange = args['framerange']

    # cr = ChronoRender()
    # cr.createAndRunRenderJob(md, stream, frange)

# def startDistributedJob(args):
    # md = verifyMetadata(args)
    # stream = args['renderer']

# def updateJobAssets(args):
    # md = verifyMetadata(args)
    # cr = ChronoRender()
    # cr.updateJobAssets(md)

# def verifyMetadata(args):
    # if not args['metadata']:
        # printErrorAndExit('no metadata specified')
    # if not os.path.exists(args['metadata']):
        # printErrorAndExit('metadata does not exist: ' + str(args['metadata']))
    # return args['metadata']

# def printErrorAndExit(msg):
    # print "ERROR:", msg
    # exit()

if __name__ == '__main__':
    main()
