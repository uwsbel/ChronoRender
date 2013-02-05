#!/usr/bin/env python
import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender

class CRenderUpdate(Prog):
    def __init__(self):
        super(CRenderUpdate, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        self.args = self.parseArgs()
        self.updateJobAssets()

    def getArgs(self):
        return { 'metadata' : ''}

    def parseArgs(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-m', '--metadata', help='the data file that contains the \
                render job info', required=False)
        return vars(parser.parse_args())

    def verifyMetaData(self):
        return super(CRenderUpdate, self).verifyMetaData()

    def updateJobAssets(self):
        md = self.verifyMetaData()
        cr = ChronoRender()
        job = cr.createJob(md)
        cr.updateJobAssets(job)

if __name__ == '__main__':
    cr = CRenderUpdate()
    cr.main()
