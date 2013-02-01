import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender

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
                default=None,
                type=int,
                required=False)
        return vars(parser.parse_args())

    def startDistributedJob(self):
        md = self.verifyMetadata()
        stream = args['renderer']

        #cr = ChronoRender()
        #cr.createAndSubmitRenderJob(md, stream)

    def verifyMetadata(self):
        if not self.args['metadata']:
            self.printErrorAndExit('no metadata specified')
        if not os.path.exists(self.args['metadata']):
            self.printErrorAndExit('metadata does not exist: ' + str(self.args['metadata']))
        return self.args['metadata']

if __name__ == '__main__':
    cr = CRenderDist()
    cr.main()
