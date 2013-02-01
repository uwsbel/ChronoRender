import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender

class CRenderLocal(Prog):
    def __init__(self):
        super(CRenderLocal, self).__init__()

    def main(self):
        self.startLocalRenderJob()

    def getArgs(self):
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
                default=None,
                type=int,
                required=False)
        return vars(parser.parse_args())

    def startLocalRenderJob(self):
        md = self.verifyMetadata()
        stream = self.args['renderer']
        frange = self.args['framerange']

        cr = ChronoRender()
        cr.createAndRunRenderJob(md, stream, frange)

    def verifyMetadata(self):
        if not self.args['metadata']:
            self.printErrorAndExit('no metadata specified')
        if not os.path.exists(self.args['metadata']):
            self.printErrorAndExit('metadata does not exist: ' + str(self.args['metadata']))
        return self.args['metadata']

if __name__ == '__main__':
    cr = CRenderLocal()
    cr.main()
