Chrono::Render
==============
![CRLogo](images/ChronoRenderLogo_100px.png)

Description
-----------
Chrono::Render is a RenderMan framework intended to offer automated, service-oriented rendering for scientific visualization.  The software package offers a compiled Python library which provides functionality for rendering with RenderMan-compliant renderers.  This functionality is made available via a succint hierarchical data specification (XML, YAML, JSON)  which configures the program to generate job-specific RenderMan api calls; this separation allows Chrono::Render to easily be glued with arbitrary processes (see [Autodesk Maya Plugin](maya/index.html)).  Additionally, Chrono::Render exposes a stream-lined scripting and plug-in interface for managing specific visualizations or for extending the software to suit individual needs.

Chrono::Render is a data-centric application and takes tagged arbitrary data sets

Distribution
-----------
crender.py
renders everything specified in the supplied hierarchical-data

crender_sim.py
renders the simulation elements (see [Data Specification](spec/index.html)) specified in the supplied hierarchical-data

cmovie.py
encodes a sequence of frames into a movie using a variety of codecs.  Used for post-processing a render if video encoding is not specified in the hierarchical-data spec (see [Data Specification](spec/index.html)) specified in the supplied hierarchical-data

ChronoRender Python Package

Tutorials
----
* Main Page [here](tutorials/index.html)

Data Specification
-----
* Main Page [here](spec/index.html)

Applications
-----
* Autodesk Maya [here](maya/index.html)
