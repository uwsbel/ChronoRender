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

    def updateJobAssets(self):
        md = self.verifyMetadata()
        cr = ChronoRender()
        cr.updateJobAssets(md)

    def verifyMetadata(self):
        if not self.args['metadata']:
            self.printErrorAndExit('no metadata specified')
        if not os.path.exists(self.args['metadata']):
            self.printErrorAndExit('metadata does not exist: ' + str(self.args['metadata']))
        return self.args['metadata']

if __name__ == '__main__':
    cr = CRenderUpdate()
    cr.main()
