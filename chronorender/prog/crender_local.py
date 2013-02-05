#!/usr/bin/env python
import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender

class CRenderLocal(Prog):
    def __init__(self):
        super(CRenderLocal, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        self.args = self.parseArgs()
        self.startLocalRenderJob()

    def getArgs(self):
        return { 'metadata' : '',
                 'renderer' : '',
                 'framerange' : None}

    def parseArgs(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-m', '--metadata', help='the data file that contains the \
                render job info', required=False)

        parser.add_argument('-r', '--renderer', 
                help='which renderer to use, dumps to stdout by default', 
                default='stdout',
                required=False)

        parser.add_argument('-f', '--framerange',
                nargs=2,
                help='render the specified framerange; by default renders all frames',
                default=[0,0],
                type=int,
                required=False)
        return vars(parser.parse_args())

    def verifyMetaData(self):
        return super(CRenderLocal, self).verifyMetaData()

    def startLocalRenderJob(self):
        md = self.verifyMetaData()
        stream = self.args['renderer']
        frange = self.args['framerange']

        cr = ChronoRender()
        job = cr.createJob(md)
        cr.runRenderJob(job, frange)

if __name__ == '__main__':
    cr = CRenderLocal()
    cr.main()
