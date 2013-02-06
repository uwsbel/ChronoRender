0) Copy all of the RMS_* dirs to your maya/projects directory

1) Set Environment Variables For MAYA and RMS, in:
maya/version/Maya.env

Windows and Linux:
RMS_SCRIPT_PATHS=$MAYA_APP_DIR/projects/RMS_ini
MAYA_SCRIPT_PATH=$MAYA_APP_DIR/projects/RMS_mel

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
