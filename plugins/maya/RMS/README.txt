REQUIRES:
Python 2.7  or greater

0) Copy all of the RMS_* dirs to your maya/projects directory

1) Set Environment Variables For MAYA and RMS, in:
maya/version/Maya.env

Windows and Linux:
RMS_SCRIPT_PATHS=$MAYA_APP_DIR/projects/RMS_ini
MAYA_SCRIPT_PATH=$MAYA_APP_DIR/projects/RMS_mel

Also For
Pixar/RMS_DIR/etc/RMSWorkspace.ini

ADD '.' to the following

SetPref WSSearchPaths.procedural \
    [list \\\${RMSTREE}/lib/plugins \\\${RMANTREE}/etc @ .]
SetPref WSSearchPaths.shader \
    [concat $stdplaces [list \\\${RMSTREE}/lib/shaders/ @ .]]
SetPref WSSearchPaths.texture \
    [concat $stdplaces [list \\\${RMSTREE}/lib/textures/ @ .]]

2) it.ini
change paths for your machine

3) RenderMan_for_Maya.ini
change paths for your machine

3) slim.ini
change paths for your machine

4) userSetup.mel
change paths for your machine

5) Open Maya

6) Enter into the MEL command line:
source "userSetup.mel";

hit Cntrl-Enter

this will source the remaining directories

7) Make Sure The RenderMan_for_Maya plugin

MAKE SURE TO ADD THE FOLLOWING ENV VARIABLES:
1) CRENDER_PATH=path_to_ChronoRender_root
2) PYTHONPATH=$PYTHONPATH:$CRENDER_PATH

-----
Batch Rendering
1    Set the Maya project directory.
2    Create a render camera
3    Save the Maya scene.
4    In Render Setting:
      - set the start and end frames,
      - set name.#.ext,
      - set 4 digits of padding,
      - set "Image Format" to an appropriate type.
      - set the Renderable Camera to the camera added earlier
5    In the script editor (MEL) execute the following command,
              batchRenderRI("", 1);

------
TIPS

1) Make sure to attach shaders to RenderObjects before export, otherwise the geometry won't be exported

2) Make sure to check Export Shaders on RIB_Archive export:
  - go to File-> Export-> RIB_Archive
