from __future__ import division
import argparse
import math
import subprocess
import sys

def parseArgs():
    parser = argparse.ArgumentParser()

    parser.add_argument('-m', '--metadata', help='the data file that contains the \
            render job info', required=False)

    parser.add_argument('-r', '--renderer', 
            help='which renderer to use, dumps to stdout by default', 
            default='stdout',
            required=False)

    parser.add_argument('-f', '--framerange',
            nargs=2,
            help='render the specified framerange; by default renders frame 0',
            default=[0,0],
            type=int,
            required=False)
    
    parser.add_argument('-c', '--name',
            help='the name of the job you are submitting. What it is (c)alled',
            default='render_job_default_name',
            required=False)

    parser.add_argument('-n', '--nodes',
            help='the number of nodes.',
            default=1,
            type=int,
            required=False)

    parser.add_argument('-i', '--instances',
            help='the number of prman instances. (max 5 can run at the same time on euler.) Also known as the number of jobs this framerange is broken up into.',
            default=1,
            type=int,
            required=False)

    parser.add_argument('-p', '--ppn',
            help='the number of cores per node. For prman, this means the number of cores one instance of prman uses (max 32 on euler)',
            default=1,
            type=int,
            required=False)

        # parser.add_argument('-g', '--gpus',
    #         help='number of gpus per node',
    #         default=0,
    #         required=False)

    parser.add_argument('-w', '--walltime',
            help='limit on how long the job can run HH:MM:SS',
            default='01:00:00',
            required=False)

    parser.add_argument('-q', '--queue',
            help='which queue to submit the job to',
            default='prman',
            required=False)

    return vars(parser.parse_args(sys.argv[2:]))

def write_script(args, name, frame_begin, frame_end, filename):
    f = open(filename, "w")

    f.write("#!/bin/sh\n\n")
    f.write("#PBS -N {0}\n".format(name))
    f.write("#PBS -l nodes={0}:ppn={1},walltime={2}\n".format(args["nodes"], args["ppn"], args["walltime"]))
    f.write("#PBS -q {0}\n".format(args["queue"]))
    f.write("\n")
    f.write("cd $PBS_O_WORKDIR\n")
    f.write("{0} render -m {1} -r {2} -f {3} {4}".format(sys.argv[0], args["metadata"], args["renderer"], frame_begin, frame_end))
    
    f.close()

def submit_qsub_script(): 
    """docstring for generate_qsub_script"""
    args = parseArgs()

    if args["renderer"] == "aqsis": 
        jobs = []
        for i in xrange(args["framerange"][0], args["framerange"][1]+1):
            filename = "qsub_submit_script{0}.sh".format(i)
            write_script(args, args["name"]+"-"+str(i), i, i, filename)
            subprocess.Popen(["qsub", "./" + filename])

    if args["renderer"] == "prman":
        difference = args["framerange"][1] - args["framerange"][0]
        fract = int(math.ceil(difference / int(args["instances"])))

        assert args["instances"] <= difference

        for i in xrange(0, args["instances"]):
            filename="qsub_submit_script_part{0}.sh".format(i)

            minframe = args["framerange"][0] + (i+1)*fract -1
            if i == args["instances"] - 1:
                minframe = args["framerange"][1]
            write_script(args, args["name"], args["framerange"][0] + i*fract, minframe, filename)
            subprocess.Popen(["qsub", "./" + filename])
