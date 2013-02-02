#!/usr/bin/env python
import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender

class CRenderInit(Prog):
    def __init__(self):
        super(CRenderInit, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        self.args = self.parseArgs()
        self.initNewRenderJob()

    def getArgs(self):
        return { 'outpath' : ''}

    def parseArgs(self):
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-o', '--outpath', help='used with init, where to \
                generate the render files; cwd if not set', required=False)

        return vars(parser.parse_args())

    def initNewRenderJob(self):
        path = self.args['outpath'] if self.args['outpath'] else os.getcwd()

        cr = ChronoRender()
        cr.generateRenderJobToDisk(path)

if __name__ == '__main__':
    cr = CRenderInit()
    cr.main()
