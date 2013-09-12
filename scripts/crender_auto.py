#!/usr/bin/env python
import tarfile
import os
import crender

def render(path_to_data_archive, path_to_metadata_archive, root_render_folder, frames=(0,0), renderer="aqsis", job_name="default_render_job_name", num_nodes=1, num_prman_instances=1, ppn=1, walltime="1:00:00", queue="prman", overwrite_data = True):

    
    crender.main(["crender.py", "init"])
    metadata = tarfile.open(path_to_metadata_archive)

    #TODO: tarfile extraction unsafe?
    metadata.extractall(os.path.join(root_render_folder, "RENDERMAN"))
    metadata.close()

    num_data_files = os.listdir(os.path.join(root_render_folder, "RENDERMAN", "job", "data"))

    if overwrite_data or len(num_data_files) > 0:
        data = tarfile.open(path_to_data_archive)
        data.extractall(os.path.join(root_render_folder, "RENDERMAN"))
        data.close()

    metadata_file = os.path.basename(path_to_metadata_archive).split(".")[0] + ".yaml"
    metadata_path = os.path.join(root_render_folder, "RENDERMAN", metadata_file)

    import pdb; pdb.set_trace()
    crender.main(["crender.py", "submit", "-m", metadata_path, "-r", renderer, "-f", frames[0], frames[1], "-c", job_name, "-n", num_nodes, "-i", num_prman_instances, "-p", ppn, "-w", walltime, "-q", queue])

    #TODO: why doesn't it render???
    #TODO: video!

def main():
    #TEST hardcoded
    render("/home/dankaczma/demo/data.tar.gz", "/home/dankaczma/demo/out.tar.gz", "/home/dankaczma/demo")


if __name__ == '__main__':
    main()
