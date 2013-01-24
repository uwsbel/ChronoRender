import os, sys
from cgkit.ribexport import *
from cgkit.pluginmanager import *

class CRenderRIBExporter(RIBExporter):
    def exportFile(self,
                   filename,
                   shader_outpath = "",
                   texture_outpath = "",
                   archive_outpath = "",
                   camera = None,
                   output = None,
                   output_framebuffer = True,
                   bake = False,
                   bakemodel = None,
                   bakestvar = "st"):
        """Export a RIB file.

        \a camera is the camera object to use. If None is passed, the
        first camera found is used.
        \a output is the output file name or a list of output specifiers
                  (which contain the parameters for a RiDisplay() call). If
                  output is None, no RiDisplay() call is done.
        """

        scene = getScene()
        self.timestep = scene.timer().timestep
        frameNr = int(round(scene.timer().frame))
        self.bake = bake

        # A list with all light sources in the scene
        # (the items are the original lights, *not* the adapted lights)
        self.lights = []
        
        # A dictionary that stores lightsource shader names
        # Key is the light class, value is the shader name
        self.light_shader = {}

        # A dictionary that stores the passes created by light sources
        # Key is the original light instance, value is the passes list
        # Empty lists are not stored.
        self.light_passes = {}

        # A dictionary that stores material shader names
        # Key is the tuple (material class, surface shader name, displacement
        # shader name, interior name), value are the shader names (surface,
        # displacement, interior)
        # (the shader names in the key are not the true file names but
        # the names returned by the material)
        self.material_shaders = {}

        # A dictionary that stores the passes created by materials
        # Key is the original material instance, value is the passes list
        # Empty lists are not stored.
        self.material_passes = {}

        # A dictionary with map names used so far
        self.mapnames = {}

        # The shader names created so far (this dictionary is used to
        # create unique file names)
        self.shader_names = {}

        # Key: (geom, matid)  Value: File name
        self.geom_file = {}
        
        # The geom file names creates so far
        # (this dictionary is used to create unique file names)
        self.geom_names = {}

        # Directory names
        self.shader_path = shader_outpath
        self.map_path = texture_outpath
        self.geom_path = archive_outpath

        filepath, filename = os.path.split(filename)
        # self.geom_path= os.path.join(filepath, self.geom_path)
        # self.shader_path= os.path.join(filepath, self.shader_path)
        # self.map_path= os.path.join(filepath, self.map_path)

        # The list with render passes
        passes = []

        # Search for a camera and collect the passes...
        cam = camera
        self.preprocess_called = {}
        for obj in scene.walkWorld():
            if cam==None and ICamera in obj.protocols():
                cam = obj

            # Check if the object is a light source
            try:
                # TODO NOT WORKING!!!
                pass 
                # explgt = protocols.adapt(obj, ILightSource)
                # self.lights.append(obj)
                # Create the RenderPass objects required for this light
                # lgtpasses = explgt.createPasses()
                # lgtpasses = self.makePassOutputUnique(lgtpasses)
                # if lgtpasses!=[]:
                    # self.light_passes[obj] = lgtpasses
                    # passes += lgtpasses
            except NotImplementedError:
                # TODO: Use protocols instead of isinstance()
                if isinstance(obj, lightsource.LightSource):
                    print 'Unknown light source: "%s"'%obj.name

            if obj.geom==None:
                continue

            #DON"T PREPROCESS MATS IN RIBs, JUST DUMP TO FOLDER AND SCRIPT
            #if obj.visible:
                #for i in range(obj.getNumMaterials()):
                    #mat = obj.getMaterial(i)
                    #if mat not in self.material_passes:
                        #try:
                            #expmat = protocols.adapt(mat, IMaterial)
                            #ps = expmat.createPasses()
                            #ps = self.makePassOutputUnique(ps)
                            #if ps!=[]:
                                #self.material_passes[mat] = ps
                                #passes += ps
                            #if mat not in self.preprocess_called:
                                #expmat.preProcess(self)
                                #self.preprocess_called[mat] = 1
                        #except NotImplementedError:
                            #pass

        if cam==None:
            cam = TargetCamera()

        # Store the camera so that Pass objects can access it
        self.cam = cam

        # Add the map path to the map names
        # (on win32, a backslash is replaced by two backslashes because
        # a renderer might interpret a single backslash as an escape character
        # (such as 3Delight))
        for ps in passes:
            tab = ps.getFilenameTable()
            for vname in tab:
                rname = tab[vname]
                rname = os.path.join(self.map_path, rname)
                if sys.platform=="win32":
                    rname = rname.replace('\\', "\\\\")
                tab[vname] = rname
            ps.setFilenameTable(tab)

        if len(passes)>0:
            self.checkMapPath()

        # Add the final image pass as last pass
#        if output==None:
#            output = scene.getGlobal("output", "out.tif")
        if bake:
            defaultdisplaymode = RI_RGBA
        else:
            defaultdisplaymode = RI_RGB
        mode = scene.getGlobal("displaymode", defaultdisplaymode)
        dispType = scene.getGlobal("displaytype", RI_FILE)
        out = self.outputSpec(output, mode=mode, output_framebuffer=output_framebuffer, display=dispType)
        if bake:
            bakemodel = cmds.worldObject(bakemodel)
            bakepass = BakePass(output=out, bakemodel=bakemodel, bakestvar=bakestvar)
            passes.append(bakepass)
        else:
            imgpass = ImagePass(output=out, cam=cam)
            passes.append(imgpass)

        # Initialize the exporter attribute in the passes...
        for p in passes:
            p.exporter = self

        # Start export...
        if not os.path.exists(self.geom_path):
            os.mkdir(self.geom_path)
            
        outfile = os.path.join(self.geom_path, filename)
        RiBegin(outfile)

        # RiOption("searchpath", "shader", "%s:&"%self.shader_path)
        # RiOption("searchpath", "archive", "%s:&"%self.geom_path)
        # RiOption("searchpath", "texture", "%s:&"%self.map_path)
        # RiHider(RI_HIDDEN, "string depthfilter", "midpoint")
        globalrib = scene.getGlobal("rib", None)
        if globalrib!=None:
            RiArchiveRecord(RI_VERBATIM, globalrib+"\n")

        # Do render passes...
        print len(passes),"passes..."
#        nr = 0
        # Tex passes first
        for rpass in passes:
            if isinstance(rpass, TexPass):
#                nr+=1
#                print "\015Pass %d..."%nr,
                rpass.doPass(frameNr)
                rpass._done = True

        # Other passes...
        for rpass in passes:
            if isinstance(rpass, TexPass):
                continue
#            nr+=1
#            print "\015Pass %d..."%nr,
            rpass.doPass(frameNr)
            rpass._done = True

        RiEnd()
        return outfile

    ## protected:
######################################################################

# RenderPass
class RenderPass:
    """RenderPass.

    A pass object can access the exporter (RIBExport) via self.exporter.
    """
    def __init__(self, output, owner=None):
        """Constructor.
        
        output is a list of output specifications that contain the
        output file name, the output type and the output mode (RI_RGB,
        RI_RGBA,...) and optional extra parameters. It's all the
        information that's necessary for a RiDisplay() call.
			
        \param owner (\c Component) The object that requires the result of this pass
        """
        self.owner = owner
        self.output = output
        # A reference to the exporter class (this is initialized in the
        # exporter after the Passes were created)
        self.exporter = None

        # done flag (this is set to True in the exporter)
        self._done = False

        # Filename table. Key: Logical file name / Value: Real filename
        self.filenametab = {}
        for name,type,mode,params in output:
            self.filenametab[name] = name

    # done
    def done(self):
        """Check if this pass is already done or not.

        This method is used when shader parameters have to be determined.
        The output of a pass may only be used once the pass is done and
        the output really exists (for example, you can't use a shadow map
        until it was created).

        \return True if the pass was already rendered (i.e. the output images exist).
        """
        return self._done

    # realFilename
    def realFilename(self, filename):
        """Translate a logical file name into a real file name.

        \param filename (\c str) Logical file name
        """
        if filename not in self.filenametab:
            raise ValueError('File name "%s" is not an output file name.'%filename)

        return self.filenametab[filename]

    # getFilenameTable
    def getFilenameTable(self):
        """Return the filename translation table.

        \return The filename translation dictionary.
        """
        return self.filenametab

    # setFilenameTable
    def setFilenameTable(self, tab):
        """Set an updated filename table.

        \param tab (\c dict) The new filename translation dictionary.
        """
        self.filenametab = tab

    # doPass
    def doPass(self, framenr):
        """Write a Frame block.

        \param framenr (\c int) Frame number to use
        """
        pass

    # initDisplays
    def initDisplays(self):
        """Call RiDisplay() for all outputs stored in the class."""
        # Do RiDisplay() calls...
        append_plus = False
        for name,type,mode,params in self.output:
            name = self.realFilename(name)
            if append_plus:
                name = "+"+name
            RiDisplay(name, type, mode, params)
            append_plus = True

        

# ImagePass
class ImagePass(RenderPass):
    def __init__(self, output, cam):
        RenderPass.__init__(self, output, None)
        self.cam = cam

    # doPass
    def doPass(self, framenr):
        scene = getScene()
        # Set light sources...
        for lgt in self.exporter.lights:
            RiAttributeBegin()
            RiAttribute("identifier", "name", lgt.name)
            RiConcatTransform(lgt.worldtransform.toList())
            # Custom RIB
            rib = getattr(lgt, "rib", None)
            if rib is not None:
                RiArchiveRecord(RI_VERBATIM, rib+"\n")
            lid = self.exporter.applyLightSource(lgt)
            RiAttributeEnd()
            if lid!=None:
                RiIlluminate(lid, lgt.enabled)
            
#            shader,params,transform,name = exporter.light_shaders[lgt]
#            lid = RiLightSource(shader, params)

        self.renderChilds(scene.worldRoot())
        
    def renderChilds(self, obj):
        exporter = self.exporter
        for child in obj.iterChilds():
            if not child.visible:
                continue
            # No geometry and no children? Then ignore this node
            if child.geom==None and child.lenChilds()==0:
                continue
#            if not exporter.isExportable(child):
#                continue

            RiAttributeBegin()
            
            # Store the name of the object
            RiAttribute("identifier", "name", child.name)
            # Transform the object
            exporter.applyTransformation(child.localTransform(), child.linearvel, child.angularvel)

            for i in range(child.getNumMaterials()):
                # Set shaders...
                exporter.applyMaterial(child.getMaterial(i))

                # Custom RIB
                rib = getattr(child, "rib", None)
                if rib!=None:
                    RiArchiveRecord(RI_VERBATIM, rib+"\n")

                # Output geometry
                exporter.applyGeometry(child.geom, i)
            
            # Recursively render all childs
            self.renderChilds(child)
            
            RiAttributeEnd()


# ShadowPass
class ShadowPass(RenderPass):
    def __init__(self, output, light, fov, resolution, orientoffset=mat4(1)):
        RenderPass.__init__(self, output, None)
        self.light = light
        self.fov = fov
        self.resolution = resolution
        self.orientoffset = orientoffset

    # doPass
    def doPass(self, framenr):
        scene = getScene()

        RiArchiveRecord(RI_COMMENT, "")
        RiArchiveRecord(RI_COMMENT, "Shadow pass")
        RiArchiveRecord(RI_COMMENT, "")
        RiFrameBegin(framenr)

        RiPixelSamples(1,1)
        RiPixelFilter(RiBoxFilter, 1, 1)
        RiFormat(self.resolution, self.resolution, 1)
        RiShadingRate(2)

        # Do RiDisplay() calls...
        self.initDisplays()

        # Camera...
        RiProjection(RI_PERSPECTIVE, fov=self.fov)
        V = (self.light.transform*self.orientoffset).inverse()
        self.exporter.applyViewTransform(V)
        RiShutter(0,1)

        RiWorldBegin()

        self.renderChilds(scene.worldRoot())
        
        RiWorldEnd()     
        RiFrameEnd()
        zname = self.realFilename(self.output[0][0])
        mapname = os.path.splitext(zname)[0]+".map"
        RiMakeShadow(zname, mapname)

    def renderChilds(self, obj):
        exporter = self.exporter
        for child in obj.iterChilds():
            if not child.visible:
                continue
            # No geometry and no children? Then ignore this node
            if child.geom==None and child.lenChilds()==0:
                continue
#            if not exporter.isExportable(child):
#                continue

            RiAttributeBegin()

            # Store the name of the object
            RiAttribute("identifier", "name", child.name)
            # Transform the object
            exporter.applyTransformation(child.localTransform())
            for i in range(child.getNumMaterials()):
                # Set shaders...
                exporter.applyMaterial(child.getMaterial(i))

                # Custom RIB
                rib = getattr(child, "rib", None)
                if rib!=None:
                    RiArchiveRecord(RI_VERBATIM, rib+"\n")

                # Output geometry
                exporter.applyGeometry(child.geom, i)
            
            # Recursively render all childs
            self.renderChilds(child)

            RiAttributeEnd()

# FlatReflectionPass
class FlatReflectionPass(RenderPass):
    def __init__(self, output, mirrorobj=None):
        RenderPass.__init__(self, output, None)
        self.mirrorobj = mirrorobj

    # doPass
    def doPass(self, framenr):
        scene = getScene()

        RiArchiveRecord(RI_COMMENT, "(Flat) Reflection pass")
        RiFrameBegin(framenr)

        RiPixelSamples(2,2)
        RiFormat(640,480,1)
        RiShadingRate(1)

        # Do RiDisplay() calls...
        self.initDisplays()

        # Camera...
        cam = self.exporter.cam
        RiProjection(RI_PERSPECTIVE, fov=cam.fov)
        self.exporter.applyViewTransform(cam.viewTransformation())
        RiScale(1,1,-1)
        RiShutter(0,1)
#        RiTranslate(0,0,1)

        RiWorldBegin()

        # Set light sources...
        for lgt in self.exporter.lights:
            RiAttributeBegin()
            RiAttribute("identifier", "name", lgt.name)
            RiConcatTransform(lgt.worldtransform.toList())
            lid = self.exporter.applyLightSource(lgt)
            RiAttributeEnd()
            if lid!=None:
                RiIlluminate(lid, RI_TRUE)
            
#            shader,params,transform,name = exporter.light_shaders[lgt]
#            lid = RiLightSource(shader, params)

        self.renderChilds(scene.worldRoot())
        
        RiWorldEnd()     
        RiFrameEnd()
        tifname = self.realFilename(self.output[0][0])
        texname = os.path.splitext(tifname)[0]+".tex"
        RiMakeTexture(tifname, texname, RI_CLAMP, RI_CLAMP, RiGaussianFilter, 1, 1)


    def renderChilds(self, obj):
        exporter = self.exporter
        for child in obj.iterChilds():
            if child==self.mirrorobj:
                continue
            if not child.visible:
                continue
#            if not exporter.isExportable(child):
#                continue

            RiAttributeBegin()
            
            # Store the name of the object
            RiAttribute("identifier", "name", child.name)
            # Transform the object
            exporter.applyTransformation(child.localTransform(), child.linearvel, child.angularvel)
            for i in range(child.getNumMaterials()):
                # Set shaders...
                exporter.applyMaterial(child.getMaterial(i))

                # Custom RIB
                rib = getattr(child, "rib", None)
                if rib!=None:
                    RiArchiveRecord(RI_VERBATIM, rib+"\n")

                # Output geometry
                exporter.applyGeometry(child.geom, i)
            
            # Recursively render all childs
            self.renderChilds(child)
            
            RiAttributeEnd()

# BakePass
class BakePass(RenderPass):
    """Create a bake pass.

    The class uses the technique described in the "Stupid RAT Tricks 2001":
    "The RenderMan EasyBake Oven" by Jonathan Litt and Dan Goldman.
    http://www.cs.washington.edu/homes/dgoldman/ezbake/EZ_Bake_Oven.htm

    Additionally, the original geometry is also stored so that raytracing
    can also be used.
    """
    
    def __init__(self, output, bakemodel, bakestvar="st"):
        """
        bakemodel is the WorldObject whose texture should be baked.
        bakestvar is the name of the variable that holds the texture
        coordinates for baking.
        """
        RenderPass.__init__(self, output, None)
        self.bakemodel = bakemodel
        self.bakestvar = bakestvar

    # doPass
    def doPass(self, framenr):
        scene = getScene()

        RiArchiveRecord(RI_COMMENT, "")
        RiArchiveRecord(RI_COMMENT, "Bake pass")
        RiArchiveRecord(RI_COMMENT, "")
        RiFrameBegin(framenr)

        i,j = scene.getGlobal("pixelsamples", (2,2))
        RiPixelSamples(i,j)
        res = scene.getGlobal("resolution", (256,256))
        try:
            if len(res)==2:
                w,h = res
                aspect = 1
            elif len(res)==3:
                w,h,aspect = res
            else:
                raise Exception
        except:
            print >>sys.stderr, "Error: Invalid resolution setting:",res
            w,h,aspect = 256,256,1
        RiFormat(w,h,aspect)
        RiShadingRate(scene.getGlobal("shadingrate", 1.0))

        # Do RiDisplay() calls...
        self.initDisplays()

        # Camera...
        RiProjection(RI_ORTHOGRAPHIC)
        bb = scene.boundingBox()
        bmin, bmax = bb.getBounds()
        RiScale(2,2,2)
        RiTranslate(-0.5, -0.5, -bmax.z-1)

        RiWorldBegin()

        # Set light sources...
        for lgt in self.exporter.lights:
            RiAttributeBegin()
            RiAttribute("identifier", "name", lgt.name)
            RiConcatTransform(lgt.worldtransform.toList())
            lid = self.exporter.applyLightSource(lgt)
            RiAttributeEnd()
            if lid!=None:
                RiIlluminate(lid, lgt.enabled)

        # Flattened geometry
        obj = self.bakemodel
        RiAttributeBegin()
        self.exporter.applyMaterial(obj.getMaterial(0))
#        RiCoordSysTransform("camera")
#        RiScale(2,2,2)
#        RiTranslate(-0.5,-0.5,1)
        RiTranslate(0,0, bmax.z+1.5)
        self.bakeModel(obj, self.bakestvar)
        RiAttributeEnd()

        # 3Delight attribute...
        RiAttribute("visibility", "string transmission", "opaque")
        # Pixie attribute...
        RiAttribute("visibility", "int trace", 1)
        
        self.renderChilds(scene.worldRoot())

        RiWorldEnd()     
        RiFrameEnd()

    def bakeModel(self, obj, stvarname="st"):
        """
        obj is the model that should be baked. stvarname is the name
        of the variable that holds the texture coordinates for baking.
        """

        # Check texture coordinates...
        info = obj.geom.findVariable(stvarname)
        if info==None:
            raise RuntimeError, "No variable '%s' found"%stvarname
            
        name, storage, type, mult = info

        if type!=FLOAT or mult!=2:
            raise TypeError, "variable '%s' is of wrong type"%stvarname

        if storage==FACEVARYING:
            geom = cmds.convFaceVarToVar(obj.geom)
        elif storage==VARYING:
            geom = obj.geom
        else:
            raise TypeError, "'%s' storage class %s not supported for baking"%(stvarname,storage)

        # Convert the model into a trimesh...
        if not isinstance(geom, TriMeshGeom):
            tm = TriMeshGeom()
            geom.convert(tm)
            geom = tm
        
        # Convert the tex coords into vec3s...
        st = geom.slot(stvarname)
#        print "sizes:",geom.verts.size(), st.size()
        stcoords = map(lambda x: vec3(x), st)

        # Transform the verts...
#        verts = []
#        W = obj.worldtransform
#        for i,j,k in geom.faces:
#            verts.append(W*geom.verts[i])
#            verts.append(W*geom.verts[j])
#            verts.append(W*geom.verts[k])

#        verts = 156*[(0,0,0)]

        # Create parameter list...
        W = obj.worldtransform
        params = {"P":stcoords,
                  "Pref":map(lambda x: W*x, geom.verts)}
        RiDeclare("Pref", "vertex point")
        clss = ["constant", "uniform", "varying", "vertex", "facevarying", "facevertex", "user"]
        typs = ["integer", "float", "string", "color", "point", "vector",
                "normal", "matrix", "hpoint"]
        for name, storage, type, multiplicity in geom.iterVariables():
            cls = clss[abs(storage)]
            typ = typs[abs(type)]
            if cls!="user":
                s = geom.slot(name)
                params[name] = list(s)
                if multiplicity==1:
                    decl = "%s %s"%(cls, typ)
                else:
                    decl = "%s %s[%d]"%(cls, typ, multiplicity)
                RiDeclare(name, decl)

#        RiCoordSysTransform("camera")
        RiPointsPolygons(len(geom.faces)*[3], list(geom.faces), params)

    def renderChilds(self, obj):
        exporter = self.exporter
        for child in obj.iterChilds():
            if not child.visible:
                continue
            # No geometry and no children? Then ignore this node
            if child.geom==None and child.lenChilds()==0:
                continue
#            if not exporter.isExportable(child):
#                continue

            RiAttributeBegin()
            
            # Store the name of the object
            RiAttribute("identifier", "name", child.name)
            # Transform the object
            exporter.applyTransformation(child.localTransform(), child.linearvel, child.angularvel)

            for i in range(child.getNumMaterials()):
                # Set shaders...
                exporter.applyMaterial(child.getMaterial(i))

                # Custom RIB
                rib = getattr(child, "rib", None)
                if rib!=None:
                    RiArchiveRecord(RI_VERBATIM, rib+"\n")

                # Output geometry
                exporter.applyGeometry(child.geom, i)
            
            # Recursively render all childs
            self.renderChilds(child)
            
            RiAttributeEnd()


# TexPass
class TexPass(RenderPass):
    def __init__(self, maps, output=[]):
        """Constructor.

        The map definition list contains one tuple for every map.
        The tuple is a 7-tuple with the following entries:

        - Map name (incl. path)
        - swrap ("periodic", "clamp", "black")
        - twrap ("periodic", "clamp", "black")
        - filterfunc ("gaussian", "box", "triangle", "sinc", "catmullrom", ...)
        - swidth
        - twidth
        - params - A dictionary with additional parameters

        These are the parameters for the \c RiMakeTexture() call.
        The output file name is generated from the input map name by
        replacing the suffix with "*.tex".
        
        \param maps A list with map defintions
        """
        RenderPass.__init__(self, output)
        self.maps = maps

    def doPass(self, framenr):
        
        for map,swrap,twrap,filterfunc,swidth,twidth,params in self.maps:

            # Copy the original image into the map directory and convert
            # to tif if necessary
            self.copyImageMap(map)

            # Call RiMakeTexture() to convert the .tif into .tex
            mapbase = os.path.basename(map)
            name, ext = os.path.splitext(mapbase)
            tifname = os.path.join(self.exporter.map_path, name)+".tif"
            texname = os.path.join(self.exporter.map_path, name)+".tex"
            if sys.platform=="win32":
                tifname = tifname.replace("\\", "\\\\")
                texname = texname.replace("\\", "\\\\")
            RiMakeTexture(tifname, texname,
                          swrap, twrap,
                          filterfunc, swidth, twidth, **params)

    ## protected:

    def copyImageMap(self, texmap):
        """Copy the texture map image into the map folder.

        \param texmap (\c str) Texture map name (incl. path)
        """

        self.exporter.checkMapPath()
        texname = os.path.basename(texmap)
        name, ext = os.path.splitext(texname)
        if ext.lower()!=".tif":
            print 'Converting "%s"'%texmap
            tifname = os.path.join(self.exporter.map_path, name+".tif")
            # Read original map
            try:
                img = Image.open(texmap)
            except IOError, e:
                print e
                return
            # Save map as TIF file
            img.save(tifname)
        else:
            print 'Copying "%s"'%texmap
            dest = os.path.join(self.exporter.map_path, os.path.basename(texmap))
            shutil.copyfile(texmap, dest)
