#!/usr/bin/env python
import argparse, os

from cr_prog import Prog
from crender_local import CRenderLocal
from chronorender import ChronoRender

class CRenderDist(Prog):
    def __init__(self):
        super(CRenderDist, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        self.args = self.parseArgs()
        self.startDistributedJob()

    def getArgs(self):
        return { 'metadata' : '',
                 'renderer' : 'stdout',
                 'framerange' : None}

    def parseArgs(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-m', '--metadata', help='the data file that contains the \
                render job info', required=False)

        parser.add_argument('-r', '--renderer', 
                help='which renderer to use, dumps to stdout by default', 
                default='stdout',
                required=False)

        parser.add_argument('-j', '--jobmanager', 
                choices=['torque'],
                help='specify the distrbuted job manager you are using; default=torque', 
                required=False)

        parser.add_argument('-f', '--framerange',
                nargs=2,
                help='render the specified framerange; by default renders all frames',
                default=[0,0],
                type=int,
                required=False)
        return vars(parser.parse_args())

    def verifyMetaData(self):
        return super(CRenderDist, self).verifyMetaData()

    def startDistributedJob(self):
        md = self.verifyMetaData()
        stream = self.args['renderer']
        frames = self.args['framerange']

        cr = ChronoRender()
        job = cr.createJob(md)
        job.frames = frames
        # prog = CRLocal()
        prog = CRenderLocal()
        import pdb; pdb.set_trace()
        cr.submitJob(job, prog)

if __name__ == '__main__':
    cr = CRenderDist()
    cr.main()
