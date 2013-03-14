--- 
layout: main 
title: SBEL Software 
description: Software projects in the lab
---

#Chrono::Render
![CRLogo](images/ChronoRenderLogo_100px.png)

##Description
Chrono::Render is a RenderMan framework intended to offer automated, service-oriented rendering for scientific visualization.  The software package offers a compiled Python library which provides functionality for rendering with RenderMan-compliant renderers.  This functionality is made available via a succint hierarchical data specification (XML, YAML, JSON)  which configures the program to generate job-specific RenderMan api calls; this separation allows Chrono::Render to easily be glued with arbitrary processes (see [Autodesk Maya Plugin](maya/index.html)).  Additionally, Chrono::Render exposes a stream-lined scripting and plug-in interface for managing specific visualizations or for extending the software to suit individual needs.

Chrono::Render is a data-centric application and takes tagged arbitrary data sets

##Distribution

##Scripts
###crender.py
* **init**
    + **Description:** Creates and links together the assets for the default "project" directory structure and files 
    + **Args:**
        + -o OUTPATH, --outpath OUTPATH
            + Where to generate the render files; current working directory if not set
    + **Usage:** *crender.py init (-o ./render_job)*
* **update**
    + **Description**: Makes all assets used by the "project" local when the script is called on a "project's" hierarchical data file.  Searches the filesystem and copies files to the "project's" directory structure
    + **Args:**
        + -m METADATA, --metadata METADATA
            + The data file that contains the render job info
    + **Usage:** *crender.py update -m job.yml*
* **render**
    + **Description:** Renders everything specified in the supplied hierarchical-data
    + **Args:**
        + -m METADATA, --metadata METADATA 
            + The data file that contains the render job info
        + -r RENDERER, --renderer RENDERER
            + Which renderer to link into; *stdout* if arg is not specified
            + Possible values: **prman**, **aqsis**, **pixie**, **3delight**, **stdout** 
        + -f FRAMEBEGIN FRAMEEND, --framerange FRAMEBEGIN FRAMEEND
            + What frames to render; by default renders all possible frames
    + **Usage:** *crender.py render -m job.yml -r prman -f 0 100*
* submit
    + **Description:** Same as **render** but the job is sumbited a distributed job manager 
    + **Args:**
        + -m METADATA, --metadata METADATA 
            + The data file that contains the render job info
        + -r RENDERER, --renderer RENDERER
            + Which renderer to link into; *stdout* if arg is not specified
            + Possible values: **prman**, **aqsis**, **pixie**, **3delight**, **stdout** 
        + -j MANAGER, --jobmanager MANAGER
            + Specify the distributed job manager you are using
            + Possible values: **torque**
        + -f FRAMEBEGIN FRAMEEND, --framerange FRAMEBEGIN FRAMEEND
            + What frames to render; by default renders all possible frames
    + **Usage:** *crender.py submit -m job.yml -r prman -f 0 100 -j torque*

###crender_sim.py
* RenderMan Procedural RIB program
* Renders the simulation elements (see [Data Specification](../spec/index.html)) specified in the
* **Args:**
    * METADATA
        + Data file that contains >=1 simulation elements 
    * FRAME
        + Which single frame of the simulations to render
* **Usage:**
    * *crender_sim.py job.yml 99* 

###cmovie.py
* Encodes a sequence of frames into a movie using a variety of codecs  
* Used for post-processing a render if video encoding is not specified in the hierarchical-data spec (see [Data Specification](../spec/index.html)) specified in the supplied hierarchical-data
* **Args:**
    + -p PROGRAM, --program PROGRAM
        + Executable program to use for Video Encoding
        + Possible Values: **ffmpeg**
    + -r FRAMERATE, --framerate FRAMERATE
        + Framerate
    + -res RES_X RES_Y, --resolution RES_X RES_Y
        + Output resolution
    + -c CODEC, --codec CODEC
        + Codec to compress images with
    + -b BITRATE, --bitrate BITRATE
        + Quality paramater
    + -vpreset VPRESET, --vpreset VPRESET
        + Quality preset  

###ChronoRender Python Package
* Python package that contains the logic necessary to render from the hierarchical data [spec](../spec/index.html)
* Plug-in and Scripting interface [here](../examples/index.html)

##Tutorials
* [here](tutorials/index.html)

##Data Specification
* [here](spec/index.html)

##Applications
* Autodesk Maya [here](maya/index.html)

