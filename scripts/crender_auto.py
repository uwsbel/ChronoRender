#!/usr/bin/env python
import tarfile
import subprocess
import os
import sys

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

    # import pdb; pdb.set_trace()
    crender.main([crend_path, "submit", "-m", metadata_path, "-r", renderer, "-f", str(frames[0]), str(frames[1]), "-c", str(job_name), "-n", str(num_nodes), "-i", str(num_prman_instances), "-p", str(ppn), "-w", str(walltime), "-q", str(queue)])

    #TODO: video!

def main():
    #TEST hardcoded
    render("/home/dankaczma/obj_test/data.tar.gz", "/home/dankaczma/obj_test/out.tar.gz", "/home/dankaczma/obj_test/out", frames=(0,5), ppn=4, num_nodes=1)


if __name__ == '__main__':
    main()
