# Chrono::Render Autodesk Maya Plugin

## Introduction
By integrating Chrono::Render with Autodesk's Maya and Pixar's RenderMan Studio, we can take full advantage of some powerful graphics functionality for making production-quality visualizations and re-usable assets.  This plugin is a pure Python and MEL script package that heavily utilizes pymel.

## Download

[Download Link](http://sbel.wisc.edu/Resources/Software/ChronoEngine/c_render)

## Installation
This describes some best practices for using RenderMan Studio and the Chrono::Render plugin with Maya; you do not have to follow this exactly to make it work, but this format is advised
(special thanks to Malcolm Kesson for this)

0. After downloading the plugin source, Copy all of the RMS/RMS_* dirs and userSetup.py to your maya/projects directory

1. Set Environment Variables For MAYA and RMS in maya/version/Maya.env

    ```
    RMS_SCRIPT_PATHS=$MAYA_APP_DIR/projects/RMS_ini
    MAYA_SCRIPT_PATH=$MAYA_APP_DIR/projects/RMS_mel
    ```

2. Change the paths for your machine in these files:
    * it.ini
    * RenderMan_for_Maya.ini
    * slim.ini
    * userSetup.mel

3. Open Maya

4. Enter into the MEL command line: 
    + source "userSetup.mel";
    + hit Cntrl-Enter; this will execute the command and source the remaining directories

5. Make Sure The RenderMan_for_Maya plugin is loaded
    + go to Window -> Settings/Preferences -> Plug-in Manager
    + find RenderMan For Maya and check loaded

6. Load the Chrono::Render Plugin
    + from the drop-down menu Chrono::Render -> ReImport

Add the following Environment Variables to your system:

```
  CRENDER_PATH=path_to_ChronoRender_root
  PYTHONPATH=$PYTHONPATH:$CRENDER_PATH
```

## How It Works

Chrono::Render is rendered as a procedural RIB in the Maya To RenderMan output where "crender_sim.py" is called with a generated yaml file argument "sim.yml".  This yaml file is created using the Maya scene graph and is regenerated everytime the scene is rendered.

Here is a sample of the RIB output:

## Using The Plugin

Consider Chrono::Render for Maya as the frontend for constructing hierarchical data ([see spec for more details](../spec/index.html)) with the workflow following:

1. Add an element
2. Edit the element
3. Add a child element

Chrono::Render for Maya helps build simulation visualizations, so it only contains the logic necessary to build these simulations and their respective subelements (data, renderobject, ...).

Examples:

### Create Simulation
This example recreates a portion of the tutorial in [examples](../tutorials/examples.html)

1. Click **Chrono::Render -> Create Simulation** from the drop-down menu
    + A polycube will be added to the scene named "simulation1"
    + Open the **Outliner** via **Window -> Outliner**
    + In the **Outliner**, you will see an object named "simulation1_t", this is the simulation object transform node
2. Select the simulation object by either clicking it in the **Perspective View** or the **Outliner**
3. Open the **Attribute Editor** (Cntrl-A or **Window -> Attribute Editor**)
    + Here you can see the nodes connected to the simulation object node (simulation1_t, simulation1_Shape, simulation1) and their attributes
4. Click on the simulation1 node tab and click the arrow next to **Extra Attributes**
    + Here you will see a list of the available parameters exposed by the data [spec](../spec/index.html)
5. Click **Chrono::Render -> Edit Selected**
    + This will open a window which lists the parameters seen in the above UI as well as provide some buttons for adding child elements
    + Any updates to the Attributes you make in this window will also be reflected in the **Attributed Editor** mentioned above; you can make changes to the element attributes in either this Window or the Attribute editor although the window provides extra helper functionality (such as GUI file finders) and is the only UI widget in which you can add new sub-elements
    + Child attribute options will have a drop-down Type list, these list the concrete built-in and plugin types made available by your Chrono::Render installation (any new plugins you add to your installation will show up here)
6. Choose **Type -> Data** for **Data** and Click **Add**
    + This creates a new **Data** node called "data"
    + If you check the **Outliner**, you will see there is a "plus" icon next to "simulation1"; clicking this icon will reveal the simulation node children nodes.  As you would expect, "data_t" is listed as a child
7. Select **Data** and click **Chrono::Render -> Edit Selected**
    + Choose **Format -> csv** for **Data Source** and Click **Add**
    + This add a DataSource node to the scene
8. Select the DataSource Node, click Chrono::Render -> Edit Selected
    + Fill in the parameters as per the [example](../tutorials/examples.html)
    + Click the Find Button, this will bring up a GUI file finder; you should put in the correct regex in this field
    + We are done with the Data
9. Select the Simulation element again
    + Click Chrono::Render -> Edit Selected
    + Select Type -> renderobject and click Add; a RenderObject node is created
10. Select the RenderObject node and click **Chrono::Render -> Edit Selected**
    + Update the attributes and add sub-elements in the same fashion as above
11. For some of the nodes, you may have noticed that the **Edit Window** provides and option to add a **Script**
    + Select the Simulation element again
    + Click **Chrono::Render -> Edit Selected** and add a new RenderObject; this creates a second RenderObject node which will also be parented under the Simulation object
    + Select the new RenderObject node, click **Chrono::Render -> Edit Selected**
    + Click **Add** next to Script; this adds the Script "filename" and "function" attributes to the RenderObject node; you will also notice the Script **Add** button is now greyed out
    + These attributes can be updated in the **Attribute Editor** by entering text as usual (so just select the RenderObject node, go to the **Attribute Editor** and input scripts/fluid.py and fluid_robj into the fields)
12. Once you are done creating the simulation element, it is time to render it
    + Make sure the renderer is set to RenderMan
    + Go to **Window -> Render Settings** 
    + Select **Render Using -> RenderMan**
    + Hit Render
    + This will generate the appropriate hierarchical data and insert Chrono::Render to be called as a procedural RIB

### Load Simulation
1. Click **Chrono::Render -> Load Simulation** from the drop-down menu
2. Select a previously generated hierarchical data file
3. The corresponding nodes are created in the Maya Scene
4. Update the nodes as necessary
5. Hit **Render**

### Batch Rendering For Distributed Jobs

If you do not have a job manager for distributed renders from Maya, or you want to use a different manager by choice, then you can opt to batch render RIB to disk.
This will generate a RIB file for every frame in the directory "scene/renderman/scenename/rib" 

Do the following:

1. Set the Maya project directory.
2. Create a render camera
3. Save the Maya scene.
4. In Render Settings:
    + Set the start and end frames
    + Set name.#.ext
    + Set 4 digits of padding
5. Select **Chrono::Render -> Batch RI _platform_** for your desired platform
6. Submit a job to render each frame using your desired job manager
    + Here is an example job script for Torque/PBS; put this in the scene directory (in this example it is "/home/rendering/fluid")

```
#!/bin/bash
#PBS -N fluid_prman
#PBS -l nodes=1:ppn=32
#PBS -t 0-99
#PBS -q prman
cd $PBS_O_WORKDIR
prman -t:all renderman/final_render/rib/`printf %04d $PBS_ARRAYID`/`printf %04d $PBS_ARRAYID`.rib
```

Submit this job from the parent directory of the script

```
qsub fluid/batchRender
```

### Tips

#### Use DelayedArchives for RenderObject Geometry

+ DelayedArchive is a geometry type supported by prman 
+ This type is good since its geometry is not loaded into memory until its respective bin is rendered
+ Additionally, we can use Delayed Archives to streamline integrating arbitrarily complex geometry made in Maya with Chrono::Render
+ In order to use them, do the following:
    + Create a RenderObject node as usual
    + Select **Type -> DelayedArchive** and **Add** the Geometry
    + The DelayedArchive contains a filename field, we will use RenderMan Studio functionality to get this information
    + Create any Polygon Primitive (**Create -> Polygon Primitive**)
    + Attach a shader to it
    + Select the Primitive and click the **Create Archive Node** function included with RMS
    + This will generated a polygon cube parented under the primitive
    + Select the new polycube, in the **Attribute Editor** you will see an **Update Archive** button; click this button
    + Copy the path in the **RIB Archive** field
    + Select the RenderObject node again and paste the path into the filename field
    + Make sure **zipped** is checked
    + Hit render, the archived primitive with the attached shader will now be used as geometry in the simulation 
    + Whenever you update the archived primitive in the Maya, be sure to hit the **Update Archive** button again; the changes will be propagated to the simulation

#### Toggle Rif if RenderMan Studio is Not Installed On Your Remote Render Farm

This needs to be done so shaders are correctly exported without an RMS dependency

+ Click **Chrono::Render -> Toggle Rif**
