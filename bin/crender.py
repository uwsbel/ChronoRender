import argparse, os
import script_utils as su
su.addCRToPath()

import chronorender

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['init', 'render', 'submit'])
    parser.add_argument('-o', '--outpath', help='used with init, where to generate the render files; cwd if not set', required=False)
    args = vars(parser.parse_args())

    if args['action'] == 'init':
        initNewRenderJob(args)

def initNewRenderJob(args):
        cr = chronorender.cr.ChronoRender()

        path = args['outpath'] if args['outpath'] else os.getcwd()

        cr.generateRenderJobToDisk(path)


if __name__ == '__main__':
    main()
