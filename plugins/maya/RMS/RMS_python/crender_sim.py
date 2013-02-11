#!/usr/bin/env python
import sys, string
import argparse

from chronorender.prog import Prog
from chronorender import ChronoRender
from chronorender.simulation import Simulation

class CRenderSim(Prog):
    # _RendererFactory = RendererFactory()
    def __init__(self):
        super(CRenderSim, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        err = sys.stderr
        f = open("cr_err.log", 'w')
        sys.stderr = f
        try:
            # self.args = self.parseArgs()
            # print self.args
            line = sys.stdin.readline()
            while line:
                words = string.split(line)
                self.args = {'metadata' : str(words[1]), 'framenumber' : int(words[2])}
                self.renderSimulations()
                line = sys.stdin.readline()
        except Exception as e:
            sys.stderr.write(str(e))
        finally:
            f.close()

    def getArgs(self):
        return { 'metadata' : '',
                 'framenumber' : 0 }

    def parseArgs(self):
        # parser = argparse.ArgumentParser()

        # parser.add_argument('-m', '--metadata', help='the data file that contains the simulation', required=True)
        # parser.add_argument('-f', '--framenumber', help='framenumber', required=True)
        # return vars(parser.parse_args())
        line = sys.stdin.readline()
        words = string.split(line)
        return {'metadata' : str(words[1]), 'framenumber' : int(words[2])}

    def verifyMetaData(self):
        return super(CRenderSim, self).verifyMetaData()

    def renderSimulations(self):
        md = self.verifyMetaData()
        frame = int(self.args['framenumber'])

        chron = ChronoRender()
        job = chron.createJob(md)
        job.typefilter = [Simulation]
        job.frames = [frame, frame]
        job.bOptions = False
        chron.runJob(job)

        sys.stdout.write('\377')
        sys.stdout.flush()

if __name__ == '__main__':
    cr = CRenderSim()
    cr.main()
