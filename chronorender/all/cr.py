from chronorender.cr_base import ChronoRenderBase

import chronorender.cr_constructor as cr_constructor

import chronorender.attribute as attr
import chronorender.camera as cam
import chronorender.data as data
import chronorender.dataprocess as dp
import chronorender.datasource as ds
import chronorender.distributed as distrib
import chronorender.geometry as geo
import chronorender.lighting as lighting
import chronorender.movie as mov
import chronorender.renderobject as renderobject
import chronorender.renderpass as rp
import chronorender.rendersettings as rendersettings
import chronorender.scene as scene
import chronorender.simulation as simulation
import chronorender.shader as shader
import chronorender.visualizer as visualizer
import chronorender.cr_scriptable as scriptable

class ChronoRender(ChronoRenderBase):
    def __init__(self):
        self._baseClasses = [attr.Attribute,
                        cam.Camera,
                        data.DataObject,
                        dp.DataProcess,
                        ds.DataSource,
                        distrib.Distributed,
                        geo.Geometry,
                        lighting.Lighting,
                        mov.Movie,
                        renderobject.RenderObject,
                        rp.RenderPass,
                        rp.settings.Settings,
                        rp.display.Display,
                        rendersettings.RenderSettings,
                        scene.Scene,
                        simulation.Simulation,
                        shader.Shader,
                        visualizer.Visualizer,
                        scriptable.Scriptable]


        self._pluginClasses = [attr.Attribute,
                        cam.Camera,
                        data.DataObject,
                        dp.DataProcess,
                        ds.DataSource,
                        distrib.Distributed,
                        geo.Geometry,
                        lighting.Lighting,
                        mov.Movie,
                        renderobject.RenderObject,
                        rp.RenderPass,
                        rp.settings.Settings,
                        rp.display.Display,
                        rendersettings.RenderSettings,
                        scene.Scene,
                        simulation.Simulation,
                        shader.Shader,
                        visualizer.Visualizer,
                        scriptable.Scriptable]
                        
        
        self._builtinPlugins = [dp.SelectNode,
                          ds.CSVDataSource,
                          geo.Sphere,
                          geo.File,
                          mov.FFMPEG,
                          rp.RayTracePass,
                          rp.OcclusionPass]

        self._jobs              = []
        self._constructor       = cr_constructor.CRConstructor()
        self._factories         = self._constructFactories()
