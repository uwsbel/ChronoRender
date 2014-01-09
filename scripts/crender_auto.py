#!/usr/bin/env python
import tarfile
import subprocess
import os
import sys
import argparse

import crender

def render(path_to_data_archive, path_to_metadata_archive, root_render_folder, frames=(0,0), renderer="prman", job_name="default_render_job_name", num_nodes=1, num_prman_instances=1, ppn=1, walltime="1:00:00", queue="prman", overwrite_data = True, crend_path=None):
    if crend_path == None:
        crend_path = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "crender.py")

    
    if not os.path.exists(os.path.join(root_render_folder, "RENDERMAN")):
        os.makedirs(os.path.join(root_render_folder, "RENDERMAN"))
    crender.main(["crender.py", "init", "-o", os.path.join(root_render_folder, "RENDERMAN")])
    # metadata = tarfile.open(path_to_metadata_archive)

    #TODO: tarfile extraction unsafe?
    # metadata.extractall(os.path.join(root_render_folder, "RENDERMAN"))
    # metadata.close()
    # if not os.path.exists(os.path.join(root_render_folder, "RENDERMAN")):
    #     os.makedirs(os.path.join(root_render_folder, "RENDERMAN"))
    subprocess.call(["tar", "-zxvf", path_to_metadata_archive, "-C", os.path.join(root_render_folder, "RENDERMAN")])

    num_data_files = os.listdir(os.path.join(root_render_folder, "RENDERMAN", "job", "data"))

    if overwrite_data or len(num_data_files) > 0:
        # data = tarfile.open(path_to_data_archive)
        # data.extractall(os.path.join(root_render_folder, "RENDERMAN"))
        # data.close()
        subprocess.call(["tar", "-zxvf", path_to_data_archive, "-C", os.path.join(root_render_folder, "RENDERMAN")])

    metadata_file = os.path.basename(path_to_metadata_archive).split(".")[0] + ".yaml"
    metadata_path = os.path.join(root_render_folder, "RENDERMAN", metadata_file)

    crender.main([crend_path, "submit", "-m", metadata_path, "-r", renderer, "-f", str(frames[0]), str(frames[1]), "-c", str(job_name), "-n", str(num_nodes), "-i", str(num_prman_instances), "-p", str(ppn), "-w", str(walltime), "-q", str(queue)])

    #TODO: video!

def main():
    parser  = argparse.ArgumentParser()

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

    parser.add_argument('-d', '--data',
            help='the path to the data.tar.gz file',
            default=None,
            required=True)

    parser.add_argument('-o', '--outyaml',
            help='the path to the out.tar.gz file',
            default=None,
            required=True)

    args = parser.parse_args()

    render(os.path.abspath(args.data), os.path.abspath(args.outyaml), os.path.abspath("./out"), frames=args.framerange, renderer=args.renderer, job_name=args.name, num_nodes=args.nodes, num_prman_instances=args.instances, ppn=args.ppn, walltime=args.walltime, queue=args.queue)


if __name__ == '__main__':
    main()
