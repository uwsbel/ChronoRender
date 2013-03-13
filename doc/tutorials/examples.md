--- 
layout: main 
title: SBEL Software 
description: Software projects in the lab
---

Chrono::Render Examples
=============================

Using Chrono::Render to Render
-----------------------------

In this example, we will demonstrate how to progressively refine a Chrono::Render data specification to visualize a "complex" data set.
*Input*: one hundred comma-separated value (CSV) files have been generated from a fluid simulation, they are labeled and stored in the following manner

* data/fluid_000.dat
* data/fluid_001.dat
* data/fluid_002.dat
* data/...
* data/fluid_099.dat

Each file correspondes to a timestep in the simulation.  Each line in the file corresponds to a single fluid particle, there are a million of particles per file. 
The particles are represented with the following fields separated by commas, in order:

* position_X : particle X position
* position_Y : particle Y position
* position_Z : particle Z position
* quat_X: orientation quaternion X component
* quat_Y: orientation quaternion Y component
* quat_Z: orientation quaternion Z component
* quat_W: orientation quaternion W component
* vel_X : unit velocity in X
* vel_Y : unit velocity in Y
* vel_Z : unit velocity in Z
* vel_mag : magnitude of velocity
* pressure: pressure at particle
* density : density at particle


### Simple: Defining The Simulation ###

Chrono::Render is a stage in a pipeline, it is not an end-to-end graphics application; Chrono::Render takes a database and transforms it, that is all.  The data input can effectively be anything, but it is up to the user to configure C::R to handle data that goes beyond the pale.  Chrono::Render is simple-minded, hence it only wants simple positions and rotations provided by a set of reserved tags that reference numeric values, these tags are "pos_x", "pos_y", and "pos_z" for positions and "euler_x", "euler_y", "euler_z" for rotations.  Our input data has the position values covered, let us compose some hierarchical input that will render the particles as spheres by positions

    chronorender:
      simulation:
        data:
          datasource:
           -type: "csv"
            name: "example_fluid_data"
            resource: "data/fluid_*.dat"
            fields: [["pos_x", float], 
                      ["pos_y", float],
                      ["pos_z", float]]
            delim: ","
        renderobject:
          -name: "particle"
          geometry: 
            type: "sphere"
            radius: 0.01

This yaml file denotes the expression of a simple simulation render.  The simulation object contains representations of datasources and renderobjects; datasources consist of the body of data that defines the simulation and renderobjects define this datas visual representation (see [spec](../spec/index.html) for more info).

Calling:

    crender.py -m fluid.yml -f 0 99

Results in a RIB stream on stdout which can be piped into a RenderMan renderer or saved to disk to be rendered later.  Additionally, Chrono::Render can interface directly with a renderer via dynamic link by using an additional flag (see [spec](../spec/index.html) for supported renderers); for instance you can use render with prman directly by calling

    crender.py -m fluid.yml -f 0 99 -r prman

This results in immediate rendering/no intermediate RIB.

### Less Simple: Defining Geometry  ###

So now we have 100 frames of a simple render of millions of spheres assembled in a "fluid-like" configuration, but what if we want a shape other than a sphere to represent our fluid particles?  There are a variety of supported primitives types that can be used automatically from the C::R data specification, but what if we have a weird, non-standard shape that is not supported?  Let us say that each particle should be represented as five spheres stacked on top of each other, how can we specify that in the input data?  Here is where scripting comes in; if you have a visualization need that is not avaible in the boilerplate data spec, then you can configure the render to generate whatever RIB you want via Python scripts.  Here is how it can be done in this fluid case:

* Create a directory called "scripts"
* Create a file called fluid.py
* Write a function to be override the Geometry render functionality (see [spec](../spec/index.html) for function templates)

"scripts/fluid.py"

    def fluid_geo(rib, *args, **kwargs):
      radius = 0.1
      for i in range(0, 5):
        rib.TranslateBegin()
        rib.Translate(0, i * 0.1, 0)
        rib.Sphere(radius, -radius, radius, 360)
        rib.TranslateEnd()

"fluid.yml"

    chronorender:
      simulation:
        data:
          datasource:
           -type: "csv"
            name: "example_fluid_data"
            resource: "data/fluid_*.dat"
            fields: [["pos_x", float], 
                      ["pos_y", float],
                      ["pos_z", float]]
            delim: ","
        renderobject:
          -name: "particle"
          geometry: 
            script: "scripts/fluid.py"
            function: "fluid_geo"


Call

    crender.py -m fluid.yml -f 0 99 -r prman

Will result in the same configuration as above, except now every particle consists of five sphere stacked vertically

### Even Less Simple: Converting Data  ###

Now that we have the "correct" geometry for our particles, what about the rotations?  All of these particles are perfectly vertical, which is incorrect.  As stated before, Chrono::Render wants Euler angles for orientations, but we only have quaternions in our data.  We can approach this using the same scripting capabilities we described above, but for the datasource object

* Create a quaternion to euler conversion function
* Add a function called convert_data which uses the quat2Euler helper function and stores the correct data

"fluid.py"

    def quat2Euler(q_x, q_y, q_z, q_w):
      return [e_x, e_y, e_z]

    def convert_data(data=[], *args, **kwargs):
      for entry in data
        euler = quat2Euler(entry['quat_X'], entry['quat_Y'], entry['quat_Z'], entry['quat_W'])
        entry['euler_x'] = euler[0]
        entry['euler_y'] = euler[1]
        entry['euler_z'] = euler[2]

And update the "fluid.yml" accordingly

"fluid.yml"

    chronorender:
      simulation:
        data:
          datasource:
           -type: "csv"
            name: "example_fluid_data"
            resource: "data/fluid_*.dat"
            fields: [["pos_x", float], 
                      ["pos_y", float],
                      ["pos_z", float],
                      ["quat_x", float],
                      ["quat_y", float],
                      ["quat_z", float],
                      ["quat_w", float]]
            delim: ","
            script: "scripts/fluid.py"
            function: "convert_data"
        renderobject:
          -name: "particle"
          geometry: 
            script: "scripts/fluid.py"
            function: "fluid_geo"

### Less Simpler: Visual Effects ###

Now that we have the fluid simulation profile and visuals how we want it, how about we do some cool stuff with the additional information we have available in the simulation database?  For instance, how about we color each particle according to its pressure?  Do this:

* Create a pressure color picker helper function and add it to "scripts/fluid.py"
* Add a "fluid_robj" function to the "scripts/fluid.py"

"fluid.py"

    def getPressureColor(pressure):
      red = [1.0, 0.0, 0.0]
      green = [0.0, 1.0, 0.0]
      blue = [0.0, 0.0, 1.0]
      if pressure >= 1.0:
        return red
      elif pressure >= 0.3:
        return green
      return blue

    def fluid_robj(rib, data=[], *args, **kwargs):
      robj = kwargs['robj'] if 'robj' in kwargs else None
      for entry in data:
          rib.TransformBegin()
          rib.Translate(entry['pos_x'], entry['pos_y'], entry['pos_z'])
          rib.Rotate(entry['euler_x'], 1, 0, 0)
          rib.Rotate(entry['euler_y'], 0, 1, 0)
          rib.Rotate(entry['euler_z'], 0, 0, 1)
          rib.Color(getPressureColor(entry['pressure']))
          # use the procedural geometry
          if robj:
            robj.geometry[0].render(rib)
          else:
            rib.Sphere(1,-1,1,360)
          rib.TransformEnd()

"fluid.yml"

    chronorender:
      simulation:
        data:
          datasource:
           -type: "csv"
            name: "example_fluid_data"
            resource: "data/fluid_*.dat"
            fields: [["pos_x", float], 
                      ["pos_y", float],
                      ["pos_z", float],
                      ["quat_x", float],
                      ["quat_y", float],
                      ["quat_z", float],
                      ["quat_w", float]]
            delim: ","
            script: "scripts/fluid.py"
            function: "convert_data"
        renderobject:
          -name: "particle"
           geometry: 
           script: "scripts/fluid.py"
           function: "fluid_geo"
          script: "scripts/fluid.py"
          function: "fluid_robj"

### Not Simple: Adding Features ###

Now that we have the fluid simulation profile and visuals how we want it, how about we work on incorporating some additional graphical features to make our render to start looking good.  Chrono::Render offers means to leverage core graphics features via both references to pre-made graphics assets or with Python scripting.  First and foremost, let us use some existing assets to bolster our fluid render by adding a camera, scene, and lighting setup to our data specification.  

"fluid.yml"

    chronorender:
      camera: 
        filename: "dof_camera.rib"
      lighting:
        filename: "three_point.rib"
        shader:
          - name: "env_light.sl"
            hdri: "park.hdr"
      simulation:
        data:
          datasource:
           -type: "csv"
            name: "example_fluid_data"
            resource: "data/fluid_*.dat"
            fields: [["pos_x", float], 
                      ["pos_y", float],
                      ["pos_z", float],
                      ["quat_x", float],
                      ["quat_y", float],
                      ["quat_z", float],
                      ["quat_w", float]]
            delim: ","
            script: "scripts/fluid.py"
            function: "convert_data"
        renderobject:
          -name: "particle"
           geometry: 
           script: "scripts/fluid.py"
           function: "fluid_geo"
          script: "scripts/fluid.py"
          function: "fluid_robj"

Here we have added a camera with a depth of field effect, a three-point light setup, and an environment light. Now you have got a full-blown RenderMan render with some complex graphics effects; be sure to check the [spec](../spec/index.html) for more features.

Integrating Chrono::Render as a RenderMan Procedural
----------------------------------------------------

In addition to operating as a standalone rendering tool, Chrono::Render can easily be integrated as a procedural RIB in other RenderMan contexts, see [maya](../maya/index.html) for an example
