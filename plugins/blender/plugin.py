import bpy
import math
import mathutils
import os
import yaml

#TODO: import selectable number of particles from .dat file
# be able to add materials to it
# export to renderman/rib?
# click and have all the scripts built
# one proxy object per type in a data column
# one script that prepares for cluster
# one script that does one frame for you
# file is: type, posx, posy, posz, quatenion, 3 radii things
# type goes something like 1=sphere, 2=elipsoid, 3=cube... 
# ^^ not any more!

# TODO: currently all objects represented by one proxy must have the SAME GEOMETRY
# eg. sphere radius 3, cannot also have spheres of radius 2
#
#OTHER NEEDED/WANTED INFO:
# camera loc, filepath, scaling factor, frame range, data file

#TODO: actually take input from blender for the export (a menu or something) colors and textures
#TODO: make specific colors/texturing available for non-proxy objs as well

#TODO/CHECKLIST: make file format (pos, rot, geom type, dimensions, group, velocity, pressure
# in bitbucket 
# render the file. in blender(headless?), then using renderman 
# full animation
# fancier stuff (moving camra/lights or fancy materials (shadows, reflection, ambient and global illumination)

# The input format:
#Group, Object ID, x_pos, y_pos, z_pos, euler_x, euler_y, euler_z, 
#   object_type, extra_params

bl_info = {
        "name": "Chrono::Render plugin",
        "description": "TODO",
        "author": "Daniel <Daphron> Kaczmarek",
        "version": (0, 2),
        "blender": (2, 67, 1), #TODO: find minimum version
        "location": "TODO",
        "warning": "",
        "wiki_url": "TODO",
        "tracker_url":"TODO",
        "category": "Import-Export"}

DEFAULT_COLOR = (0.4, 0.4, 0.6)

fin = ""
objects = ""
proxyObjects = ""

class Object:
    def __init__(self, data):
        # print("CREATING OBJECT")
        # print("DATA:",data)
        self.group = data[0]
        self.index = int(data[1]) #The objects unique ID/index number
        #XYZ locations
        self.x = float(data[2])
        self.y = float(data[3])
        self.z = float(data[4])
        #Euler angles x,y,z
        self.ex = float(data[5])
        self.ey = float(data[6])
        self.ez = float(data[7])

        self.obj_type = data[8].lower()
        #Extra parameters (specific to each object type)
        self.ep = [float(data[x]) for x in range(9,len(data))] 

        self.color = DEFAULT_COLOR
        self.material = self.create_material()

    def create_material(self):
        #TODO: material is created but not applied to the object!
        mat = bpy.data.materials.new("Group {}'s material".format(self.group))
        mat.diffuse_color = self.color
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        mat.specular_color = (1.0, 1.0, 1.0)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = 1.0
        mat.ambient = 1

    def addToBlender(self):
        # if self.index % 100 == 0:
            # print("index = {}".format(self.index))
        # Cube
        if self.obj_type == "cube":
            #ep[0] = length of one side
            bpy.ops.mesh.primitive_cube_add(radius=self.ep[0], location=(self.x, self.y, self.z), rotation=(self.ex, self.ey, self.ez))
        # Cylinder
        elif self.obj_type == "cylinder":
            # ep[0] = radius of top, ep[1] = depth
            bpy.ops.mesh.primitive_cylinder_add(radius=self.ep[0], depth=self.ep[1], location=(self.x, self.y, self.z), rotation=(self.ex, self.ey, self.ez))
        # Sphere
        elif self.obj_type == "sphere":
            # ep[0] = radius of the sphere
            # uv sphere looks nicer but icosphere might be the better route
            bpy.ops.mesh.primitive_uv_sphere_add(size=self.ep[0], location=(self.x, self.y, self.z), rotation=(self.ex, self.ey, self.ez))
        # Ellipsoid
        elif self.obj_type == "ellipsoid":
            #TODO: The elipses are just WRONG.
            #ep[0] is the radius, ep[1] is the length in the direction of rotation
            bpy.ops.mesh.primitive_uv_sphere_add(size=self.ep[0], location=(self.x, self.y, self.z), rotation=(self.ex, self.ey, self.ez))
            #The right way?
            bpy.ops.transform.resize(value=(1,0.5,5))
        else:
            print("Object type {} is not currently supported as a primitive")
 
        bpy.context.active_object["index"] = self.index
        bpy.context.active_object.name = "Obj # {}".format(self.index)
        bpy.context.active_object.data.materials.append(self.material)
        self.obj = bpy.context.active_object
        #object.get("index") to get the value
        #object["index"] doesn't work?

    def update(self):
        """Grabs stuff like color, texture and stores them"""
        #Color can be diffuse, specular, mirror, and subsurface scattering
        if self.obj.active_material is not None:
            self.color = (self.obj.active_material.diffuse_color[0], self.obj.active_material.diffuse_color[1], self.obj.active_material.diffuse_color[2])

class ProxyObject(Object):
    def __init__(self, data, indicies):
        """ data is a line of the input file, indicies is a list of lines 
        from the file that this obj represents whichAttribute is a num which 
        specifies the column of data on the line that decides proxyObjs and 
        group tells the specifica group which this proxyObj is for 
        (sphere, cube...) """
        # print("MAKING PROXY OBJ")

        Object.__init__(self, data)
        self.indicies = indicies
        self.group = data[0]
        # print(self.group)
        self.color = DEFAULT_COLOR
        self.obj_type = data[8].lower()
        self.ep = [float(data[x]) for x in range(9,len(data))] 
        self.material = self.create_material()

    def create_material(self):
        mat = bpy.data.materials.new("Group {}'s material".format(self.group))
        mat.diffuse_color = self.color
        mat.diffuse_shader = 'LAMBERT'
        mat.diffuse_intensity = 1.0
        mat.specular_color = (1.0, 1.0, 1.0)
        mat.specular_shader = 'COOKTORR'
        mat.specular_intensity = 0.5
        mat.alpha = 1.0
        mat.ambient = 1

    def addToBlender(self):
        # print(self.ep)
        bpy.ops.mesh.primitive_monkey_add(radius=self.ep[0], location=(self.x, self.y, self.z))
        bpy.context.active_object["group"] = self.group
        bpy.context.active_object.name = "Proxy " + self.group
        bpy.context.active_object.data.materials.append(self.material)
        self.obj = bpy.context.active_object

    def update(self):
        """Grabs stuff like color, texture and stores them"""
        #Color can be diffuse, specular, mirror, and subsurface scattering
        if self.obj.active_material is not None:
            self.color = (self.obj.active_material.diffuse_color[0], self.obj.active_material.diffuse_color[1], self.obj.active_material.diffuse_color[2])
            self.mat = self.obj.active_material

def configInitialScene():
    # bpy.ops.object.delete()
    pass

class ImportChronoRender(bpy.types.Operator):
    """Imports a ChronoRender file."""
    bl_idname = "import.import_chrono_render"
    bl_label = "Import ChronoRender"
    filename = bpy.props.StringProperty(subtype='FILE_PATH')
    directory = bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        global fin
        global objects
        global proxyObjects
        # filename = "/home/xeno/repos/blender-plugin/plugins/blender/blender_input_test.dat"
        individualObjectsIndicies = []

        objects = []
        proxyObjects = []

        filepath = os.path.join(self.directory, self.filename)

        fin = open(filepath, "r")

        for i, line in enumerate(fin):
            if i+1 in individualObjectsIndicies:
                objects.append(Object(line.split(",")))
                if i % 100 == 0:
                    print("Object {}".format(i))

            else:
                data = line.split(",")
                proxyExists = False
                for obj in proxyObjects:
                    if obj.group == data[0]:
                        obj.indicies.append(i+1)
                        proxyExists = True
                if not proxyExists:
                    print("New Proxy line num {}".format(i))
                    proxyObjects.append(ProxyObject(data, [i+1]))

        configInitialScene()

        for obj in objects:
            obj.addToBlender()
        for obj in proxyObjects:
            obj.addToBlender()

        print("objects added")
        return {'FINISHED'}

def add_importChronoRenderButton(self, context):
    self.layout.operator(
            ImportChronoRender.bl_idname,
            text=ImportChronoRender.__doc__,
            icon='PLUGIN')

class ExportChronoRender(bpy.types.Operator):
    """Exports the current scene into an easy to render format for Chrono::Render"""
    bl_idname = "export.export_chrono_render"
    bl_label = "Import Chrono::Render"
    filename = bpy.props.StringProperty(subtype='FILE_PATH')
    directory = bpy.props.StringProperty(subtype='DIR_PATH')

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        # export_filename = "/home/xeno/repos/blender-plugin/plugins/blender/blender_output_test.md"
        #TODO: get objects and proxyobject properties from blender
        # into the yaml file
        # Start by getting the global stuff to work
        global fin
        global objects
        global proxyObjects

        filepath = os.path.join(self.directory, self.filename)
        fout = open(filepath, "w")
        print("Export beginning")

        #Camera stuff
        camera_loc = bpy.data.objects['Camera'].location
        camera_rot = bpy.data.objects['Camera'].rotation_euler[0:3]
        camera_rot_degrees = [math.degrees(i) for i in camera_rot]
        cam_file_name = "custom_camera.rib"
        cam_file = open(cam_file_name, "w")
        cam_file.write('Projection "perspective" "fov" [37]\n')
        cam_file.write('Rotate {} {} {}\n'.format(camera_rot_degrees[0],
                                                camera_rot_degrees[1],
                                                camera_rot_degrees[2]))
        cam_file.write('Translate {} {} {}\n'.format(camera_loc[0],
                                                    camera_loc[1],
                                                    camera_loc[2]))
        cam_file.close()


        renderobject = []
        for proxy in proxyObjects:
            proxy.update()
            name = proxy.group
            maxIndex = max(proxy.indicies)
            minIndex = min(proxy.indicies)

            color = "{} {} {}".format(proxy.color[0], proxy.color[1], proxy.color[2])

            obj = dict()
            obj["name"] = str(name)
            obj["condition"] = "id >= {} and id <= {}".format(minIndex, maxIndex)
            obj["color"] = color
            obj["geometry"] = [{"type" : proxy.obj_type}]
            
            if proxy.obj_type.lower() == "sphere":
                obj["geometry"][0]["radius"] = proxy.ep[0]

            renderobject.append(obj)

        data = {"chronorender" : {
                    "rendersettings" : {"searchpaths" : "./"},
                    "camera" : [{"filename" : cam_file_name}],
                    "lighting" : [{"filename" : "default_lighting.rib"}],
                    "scene" : [{"filename" : "default_scene.rib"}],
                    "renderpass" : [{
                            "name" : "defaultpass",
                            "settings" : {
                                "resolution" : "640 480",
                                "display" : {"output" : "out.tif"}}}],
                    "simulation" : {
                        "data" : {
                            "datasource" : [{
                                "type" : "csv",
                                "name" : "defaultdata",
                                "resource" : "./*.dat",
                                "fields" : [
                                    ["id", "integer"],
                                    ["pos_x", "float"],
                                    ["pos_y", "float"],
                                    ["pos_z", "float"],
                                    ["euler_x", "float"],
                                    ["euler_y", "float"],
                                    ["euler_z", "float"]]}]},
                            
                            "renderobject" : renderobject}}}
                            # [{
                            #     "name" : "particle",
                            #     "condition" : "id >= 0",
                            #     "color" : color,
                            #     "geometry" : [{
                            #         "radius" : 0.888,
                            #         "type" : "sphere"}]}]}}}}

        yaml.safe_dump(data, fout)

        print("Export complete! (yes really)")
        return {'FINISHED'}

def add_exportChronoRenderButton(self, context):
    self.layout.operator(
            ExportChronoRender.bl_idname,
            text=ExportChronoRender.__doc__,
            icon='PLUGIN')

def register():
    print("Registering")
    bpy.utils.register_class(ImportChronoRender)
    # bpy.types.INFO_MT_file.append(add_object_button)
    bpy.types.INFO_MT_file_import.append(add_importChronoRenderButton)

    bpy.utils.register_class(ExportChronoRender)
    bpy.types.INFO_MT_file_export.append(add_exportChronoRenderButton)

def unregister():
    print("Unregistering")
    bpy.utils.unregister_class(ImportChronoRender)
    bpy.types.unregister_class(ExportChronoRender)


#TODO: run only when export button hit!
# fin.close()


if __name__ == "__main__":
    register()
    # main()