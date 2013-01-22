import argparse, os
import script_utils as su
su.addCRToPath()

import chronorender

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('action', choices=['init', 'render', 'submit', 'update'])

    parser.add_argument('-m', '--metadata', help='the data file that contains the \
            render job info', required=False)

    parser.add_argument('-r', '--renderer', help='which renderer to use, dumps\
    to stdout by default',required=False)

    parser.add_argument('-o', '--outpath', help='used with init, where to \
            generate the render files; cwd if not set', required=False)

    args = vars(parser.parse_args())

    if args['action'] == 'init':
        initNewRenderJob(args)
    elif args['action'] == 'render':
        startLocalRenderJob(args)
    elif args['action'] == 'submit':
        startDistributedJob(args)
    elif args['action'] == 'update':
        updateJobAssets(args)

def initNewRenderJob(args):
    path = args['outpath'] if args['outpath'] else os.getcwd()

    cr = chronorender.cr.ChronoRender()
    cr.generateRenderJobToDisk(path)

def startLocalRenderJob(args):
    md = verifyMetadata(args)

    stream = args['renderer'] if 'renderer' in args else ''

    print stream
    cr = chronorender.cr.ChronoRender()
    cr.createAndRunRenderJob(md, stream)

def startDistributedJob(args):
    md = verifyMetadata(args)

def updateJobAssets(args):
    md = verifyMetadata(args)
    cr = chronorender.cr.ChronoRender()
    cr.updateJobAssets(md)

def verifyMetadata(args):
    if not args['metadata']:
        printErrorAndExit('no metadata specified')
    if not os.path.exists(args['metadata']):
        printErrorAndExit('metadata does not exist: ' + str(args['metadata']))
    return args['metadata']

def printErrorAndExit(msg):
    print "ERROR:", msg
    exit()


if __name__ == '__main__':
    main()
