#!/usr/bin/env python
import argparse, os

from cr_prog import Prog
from chronorender.cr import ChronoRender
# from chronorender.metadata import MetaData
# from chronorender.simulation import Simulation
# from chronorender.renderer import RendererFactory

class CRenderSim(Prog):
    _RendererFactory = RendererFactory()
    def __init__(self):
        super(CRenderSim, self).__init__()
        self.path , self.name = self.getPathAndName(__file__)
        self.sims  = []
        self.cr   = ChronoRender()
        self.renderer = None

    def main(self):
        self.args = self.parseArgs()
        # self.loadSimulationFromMD()
        self.renderSimulation()
        # self.startLocalRenderJob()

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

    def loadSimulationFromMD(self):
        mdfile = self.verifyMetaData()
        md = MetaData(mdfile)
        simdata = md.listFromType(Simulation, bRequired=True)
        for data in simdata:
            sim = Simulation(factories=self.cr.getFactories(), **data)
            # sim.resolveAssets()
            self.sims.append(sim)

    def loadRenderer(self):
        md = self.verifyMetaData()
        stream = 'stdout'
        frange = self.args['framerange']

        cr = ChronoRender()
        # cr.createAndRunRenderJob(md, stream, frange)
        # self.renderer = CRenderSim._RendererFactory.build('stdout')

    def renderSimulation(self):
        fnum = self.args['framenumber']
        for sim in self.sims:
            sim.render(self.renderer, framenumber=fnum)

if __name__ == '__main__':
    cr = CRenderSim()
    cr.main()
