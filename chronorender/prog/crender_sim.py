#!/usr/bin/env python
import argparse

from cr_prog import Prog
from chronorender import ChronoRender
from chronorender.simulation import Simulation

class CRenderSim(Prog):
    # _RendererFactory = RendererFactory()
    def __init__(self):
        super(CRenderSim, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)

    def main(self):
        self.args = self.parseArgs()
        self.renderSimulations()

    def getArgs(self):
        return { 'metadata' : '',
                 'framenumber' : 0 }

    def parseArgs(self):
        parser = argparse.ArgumentParser()

        parser.add_argument('-m', '--metadata', help='the data file that contains the simulation', required=True)
        parser.add_argument('-f', '--framenumber', help='framenumber', required=True)
        return vars(parser.parse_args())

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

if __name__ == '__main__':
    cr = CRenderSim()
    cr.main()
