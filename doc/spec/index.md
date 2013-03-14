--- 
layout: main 
title: SBEL Software 
description: Software projects in the lab
---

# Chrono::Render Data Specification

# Hierarchical Data
## Root Element
* **name**: "chronorender"
* **description**: all elements under this will be read and processed by Chrono::Render 

## RenderSettings
* **name**: "rendersettings"
* **description**: high-level settings for configuring outputs and paths
* **parameters**:
  + _out_ 
      + Path/name of the output file
      + string
      + "./output/test"
  + _padding_ 
      + Number of digits to tack onto the output image sequence; evaluates to "_out_._padding_._fileformat_"
      + integer
      + 4
  + _fileformat_ 
      + The image format to render as; types available varies by renderer  
      + string
      + "jpg"
  + _searchpaths_
      + A ":" separated list of path names which will be used to find/resolve any assets (such as files or scripts)
      + string
      + ".:..:/home/graphics/ribs"

## Camera
* **name**: "camera"
* **description**: the series of RenderMan calls which specify the view transformation and camera effects (such as depth of field or lens angle)
* **parameters**:
  + _filename_
      + file which contains some RIB; can have a relative or absolute path
      + string
      + "default_camera.rib"
  + _script_
      + see **Script**

## Lighting
* **name**: "lighting"
* **description**: the series of RenderMan calls which specify the lighting setup
* **parameters**:
  + _shader_
    + see **Shader**
  + _filename_
      + file which contains some RIB; can have a relative or absolute path
      + string
      + "default_lighting.rib"
  + _script_
      + see **Script**

## Scene
* **name**: "scene"
* **description**: the series of RenderMan calls which specify additional graphics stuff (like other: geometry, lights, ...)
* **parameters**:
  + _filename_
      + file which contains some RIB; can have a relative or absolute path
      + string                        
  + _filename_

## Geometry
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Shader
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Script
* **name**: "script"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Distributed
* **name**: "distributed"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Movie
* **name**: "movie"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

# Notes
All Elements above can contain a type parameter called:

+ **name**: "type"
* **description**: the name of the concrete class type
  + returned by the class _getTypeName_ function

Given that a corresponding named factory directory exists in a plugins directory (see [plugins](../tutorials/index.html) for details).  For example, the type parameter becomes available for RenderPa
      + "default_scene.rib"
  + _script_
      + see **Script**

## RenderPass
* **name**: "renderpass"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Simulation
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Data
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## DataSource
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## DataProcess
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## RenderObject
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Geometry
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Shader
* **name**: "scene"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Script
* **name**: "script"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Distributed
* **name**: "distributed"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

## Movie
* **name**: "movie"
* **description**: all elements under this will be read and processed by Chrono::Render 
* **parameters**:
  + _filename_

# Notes
All Elements above can contain a type parameter called:

+ **name**: "type"
* **description**: the name of the concrete class type
  + returned by the class _getTypeName_ function

Given that a corresponding named factory directory exists in a plugins directory (see [plugins](../tutorials/index.html) for details).  For example, the type parameter becomes available for RenderPass elements if a directory called "plugins/renderpass" is created.  


# Supported Renderers
These are renderers that can be dyanmically linked

* Pixar PhotoRealistc Renderman "prman"
* Aqsis
* Pixie
* 3Delight
