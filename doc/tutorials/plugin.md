--- 
layout: main 
title: SBEL Software 
description: Software projects in the lab
---

Chrono::Render Plugins
=====================

Chrono::Render exposes interfaces for its main abstractions which enables a simple means to integrate new general-purpose functionality into the service.

Where Plugins Are Stored
-----------------------

Plugins are packaged in a structure with the distribution under "chronorender/plugins".

As of now, the structure is as follows:

* plugintypename1dir/
* plugintypename2dir/
* ...
* plugin_manager.yml

Each of the plugintypename directories corresponds to an extendible element of the [data specification](spec/index.html).  The files within represent concrete instances of the element base class.  At runtime, these source files are loaded and registered in factories by the plugin_manager.

Changing/Adding Plugin Paths
----------------------------

plugin_manager.yml stores configuration data for the plugin_manager

Factory plugin search paths are the only parameter as of now.  You can modify this file to point to different or additional plugin paths simply by modifying the appropriate value.  Paths are read as relative to the plugin_manager.yml location. Also, you can specify multiple plugin paths by appending them to the corresponding value and separating each path with a ":" character.

For example, to add a new absolute path for geometry plugins, you can edit the file as follows:

factory:
  ...
  geometry: "geometry:/home/shared/cr_plugins/geometry"
  ...

Creating A Plugin
----------------

Writing a plugin is more or less equivalent to writing a RenderMan DSO, except its a DSO with a sense of structured responsibility and a variety of helpful data elements and functions made available.

### DSO Equivalent : Red Sphere ###

Here is a trivial geometry plug-in which adds a red-colored sphere as a geometry element-type exposed by the Chrono::Render data specification

1) Add a file, redsphere.py to plugins/geometry

2) "redsphere.py" file source:

    from chronorender.geometry import Geometry

    class RedSphere(Geometry):
        # all factory plugin must define a static getTypeName method
        # which will be used to construct the concrete instance from
        # from the data specification
        @staticmethod
        def getTypeName():
          return 'redsphere'

        # self.radius is defined as a reference to the object member
        # for convenience sake
        def __init__(self, *args, **kwargs):
          super(RedSphere,self).__init__(*args, **kwargs)
          self.radius = self.getMember('radius')

        # function that defines the variables exposed by the data specification
        # in this case, RedSphere exposes a 'radius' float parameter which has a
        # default value of 1.0
        def _initMembersDict(self):
          super(RedSphere,self)._initMembersDict()
          self._members['radius'] = [float, 1.0]

        # if any change is made to the object's instance variables
        # they will be reflected in the member dictionary
        def updateMembers(self):
          self.setMember('radius', self.radius)

        # geometry types override a render method which produces 
        # RIB procedurally at render time
        def render(self, rib, **kwargs):
          rib.Color(1.0, 0.0, 0.0)
          rib.Sphere(self.radius, -self.radius, self.radius, 360.0) 

    # every factory type must expose a module_level build method
    # which returns an instance of the concrete type
    def build(**kwargs):
      return RedSphere(**kwargs)
      

Now that this interface is filled out, the RedSphere type is now available for use in the data specification; here's example usage in yaml:

    ...
    geometry:
      type: "redsphere"
      radius: 2.5
    ...

