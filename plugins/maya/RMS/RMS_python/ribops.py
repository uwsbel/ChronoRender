# ribops.py
# See also batchRenderRi.mel
# Version 2.2
# Oct 9 2011, Oct 16 2011, Oct 23 2011, Nov 5 2011
# 23 Jan 2012 - added render layer support
# Malcolm Kesson
# import re, os, sys, prman, subprocess, time, inspect
import re, os, sys, subprocess, time, inspect
# from MayaProjUtils import MayaProjUtils

# _utils = MayaProjUtils()

def main():
    args = sys.argv[1:]
    scene = args[0]     # remove .ma or .mb
    project = args[1]   # full path to project
    # project = os.path.join(project, 'renderman')
    begin = args[2]     # start frame
    end = args[3]       # end frame
    layer = args[4]     # render layer, example, "defaultRenderLayer"
    platform = args[5]


    # Get an instance of our rib handling class
    job = Job(project)

    ribs = job.getRMSFrameRibs(layer,scene,project,begin,end)
    roots =  ribs[0] # rib/0001/0001.rib
    finals = ribs[1] # rib/0001/perspShape_Final.0001.rib
    geoms =  ribs[2] # rib/0001/particleShape1.0001.rib + shadow passes

    # We dynamically import the Rif module(s) using __import__ and 
    # getattr() because the names of the modules are known only at runtime.
    # if len(args) == 6:
    # TODO No Rif For Now
    if False:
        if len(args[6]) > 0:
            rifs = job.getRifsFromString(args[5])
            rifs = rifs[1:]  # Ignore the first item
            geomRifs = []
            otherRifs = []
            for rif in rifs:
                if job.isGeometryRif(rif):
                    geomRifs.append(rif)
                else:
                    otherRifs.append(rif)
            # Static geometry is archived in the shared 'job' directory
            job.rifRMSJobRibs(geomRifs, scene, project)
            # Non static geometry is archived within each frame directory
            job.rifRibs(geomRifs, geoms)

            # Apply all rifs to the _Final rib(s)
            job.rifRibs(rifs, finals)

    job.renderRMSRootRibs(scene, project, roots, begin, end, platform) #scene, project, begin, end)

class Job():
    # Rifs that implement any of these methods will be applied to the archive ribs
    # in the RMS "job" directory. See isGeometryRif().
    geoMethods = ['TrimCurve','VArchiveRecord','VPAtmosphere',\
            'Blobby','Curves','Cylinder','Disk','GeneralPolygon',\
            'GeometricApproximation','Geometry', 'SubdivisionMesh',\
            'HierarchicalSubdivisionMesh','PointsGeneralPolygons',\
            'Hyperboloid','NuPatch','ObjectBegin','ObjectEnd',\
            'ObjectInstance','Paraboloid','Patch','PatchMesh',\
            'Points','PointsPolygons','Polygon','Procedural','Torus',\
            'ReadArchive','SolidBegin','SolidEnd','Sphere','Volume']
    #-------------------------------------------------
    # Constructor
    #-------------------------------------------------
    def __init__(self, logPath):
        self.logpath = logPath

    #-------------------------------------------------
    # getRifsFromString
    #-------------------------------------------------
    # For example,     
    #    rifs = getRifsFromString('rif_deepimage;rif_shadingrate')
    # Returns a list [ri, rif1, rif2 ...]
    # The first item is the instance of prman.Ri() used to
    # instantiate the rif(s)
    def getRifsFromString(self, text):
        text = text.strip()
        regx = re.compile(r'[;]')
        names = [ ]
        parts = regx.split(text)
        for part in parts:
            # Avoid empty strings
            if len(part) > 0:
                names.append(part)
        if len(names) > 0:
            return self.getRifsFromList(names)

    #-------------------------------------------------
    # getRifsFromList
    #-------------------------------------------------
    # For example,
    #    names = ['rif_deepimage','rif_shadingrate']
    #    rifs = getRifsFromList(names)    
    # Returns a list [ri, rif1, rif2 ...] the first item of which
    # is the instance of prman.Ri() used to instantiate the rif(s)
    def getRifsFromList(self, rifnames):
        out = []
        ri = prman.Ri()
        out.append(ri)
        for name in rifnames:
            cls = self.getClassFromStr(name)
            rifClass = cls[0]
            if len(cls) == 1:
                rifInst = rifClass(ri)
            else:
                rifArgs = cls[1]
                # Caller may specify multiple args as,
                # rif_foo.Rif(['group2','pCube']) 
                # or 
                # rif_foo.Rif('group2','pCube')
                rifArgs = rifArgs.strip('[]')
                regx = re.compile(r'[,]')
                parts = regx.split(rifArgs)
                args = []
                for part in parts:
                    if len(part) > 0:
                        if self.isNumber(part):
                            args.append(float(part))
                        else:
                            args.append(part)
                # We assume a single arg should NOT be passed to the
                # constructor as a list.
                if len(args) == 1:
                    rifInst = rifClass(ri,args[0])
                else:
                    rifInst = rifClass(ri,args)
            out.append(rifInst)
        return out    

    #-----------------------------------------------------
    # The module/class name string (mcStr) might be of several forms.
    # 'rif_hello'           - module name only, assume classname is 'Rif'
    # 'rif_hello.Rif'    - module + classname
    # 'rif_hello.Rif()' - module + classname + no args
    # 'rif_hello.Rif(arg1,"text")' - fully specified
    #
    def getClassFromStr(self, mcStr):
        regx = re.compile(r'[()]')
        parts = mcStr.split('.',1)
        module = parts[0]
        if len(parts) == 1:
            parts.append('Rif()')
        # Tokenize on '()' to extract any args
        tokens = regx.split(parts[1:][0])
        tokens = self.removeEmptyStrs(tokens);
        cls = tokens[0]
        argStr = ''
        if len(tokens) == 2:
            argStr = tokens[1]
        mcStr = module + '.' + cls
        parts = mcStr.split('.')
        m = __import__(module)
        for comp in parts[1:]:    
            m = getattr(m, comp)
        out = [m]
        argStr = argStr.strip()
        if len(argStr):
            out.append(argStr)
        return out

    #-------------------------------------------------
    # rifRMSFinalRibs
    #-------------------------------------------------
    # Applies the rifs to the xxx_Final.rib file(s). 
    # For example,
    #    ri = prman.Ri()
    #    rif = myRif.Ri(ri)
    #    rifRMSFinalRibs([rif], 'test', 'D:/maya/projects/DeepImage')
    # 
    def rifRMSFinalRibs(self, rifs, scene, project):
        scene = os.path.splitext(scene)[0]
        ribs = self.getRMSFinalRibs(scene, project)
        self.rifRibs(rifs,ribs)

    #-------------------------------------------------
    # rifRMSJobRibs
    #-------------------------------------------------
    # Applies the rifs to ribs in the RMS 'job' directory. 
    # For example,
    #    ri = prman.Ri()
    #    rif = myRif.Ri(ri)
    #    rifRMSJobRibs([rif], 'test', 'D:/maya/projects/DeepImage')
    # 
    def rifRMSJobRibs(self, rifs,scene, project):
        scene = os.path.splitext(scene)[0]
        ribs = self.getRMSJobRibs(scene, project)
        self.rifRibs(rifs,ribs)

    #-------------------------------------------------
    # rifRibs
    #-------------------------------------------------
    # Applies the rifs to all the ribs specified by the
    # "ribs" list.
    # For example,
    #    rifs = job.getRifsFromString('rif_deepimage,rif_shadingrate')
    #    rifs = rifs[1:]  # Ignore the first item
    #    ribs = GET SOME RIBS
    #    rifRibs(rifs, ribs)
    # 
    def rifRibs(self, rifs, ribs):
        # Get the instance of Ri used by any of the Rifs.
        # Currently there can only be a single instance of Ri
        # "shared" by the rifs so it doesn't matter which Rif
        # we use.
        if len(rifs) == 0:
            return
        ri = rifs[0].m_ri
        ri.Option("rib", {"string asciistyle": "indented"})
        prman.RifInit(rifs)
        for rib in ribs:
            parent = os.path.dirname(rib)
            name = os.path.basename(rib)
            tmpRib = os.path.join(parent, 'tmp_' + name)
            ri.Begin(tmpRib)
            prman.ParseFile(rib)
            ri.End()
            os.remove(rib)
            os.rename(tmpRib,rib)

        msg = 'Filtered %d ribs using the following,\n' % len(ribs)
        for rif in rifs:
            name = str(rif.__class__)
            msg += '  %s\n' % name[8:len(name)-2]
        self.log('log_rif.txt', msg)

    #-------------------------------------------------
    # renderRMSRootRibs
    #-------------------------------------------------
    # For example,
    #    renderRMSRootRibs('test', 'D:/maya/projects/DeepImage', 1, 30)
    # The "root" ribs are those created by RMS. They are named
    # with 4 digits ie. 0001.rib
    #
    def renderRMSRootRibs(self, scene, project, rootRibs, begin, end, platform):
        scriptpath = os.path.join(project, 'renderman')
        if len(rootRibs) > 0:
            if platform == "posix":
                batchPath = os.path.join(scriptpath, 'batchRender')
                self.makeBatchRenderScript(scene, scriptpath, 
                        batchPath, rootRibs, platform, begin, end)
                os.chmod(batchPath, 0777)
                # args = ['sh', batchPath]
            else:
                batchPath = os.path.join(scriptpath, 'batchRender.bat')
                batchPath = self.makeBatchRenderScript(scene, scriptpath, 
                        batchPath, rootRibs, platform, begin, end)
                # args = ['start', batchPath]
            # Without PIPE the process blocks when rendering to "it"
            # Don't execute
            # subprocess.Popen(args,stdout=subprocess.PIPE)
        msg = 'Job: \"%s\" in \"%s\".\n' % (scene, project)
        msg += 'Rendered frames %s to %s.\n' % (begin, end)
        self.log('log_render.txt', msg)

    # Utility_____________________________________________
    # Returns three lists. 
    # The first will have the full paths to the "root" ribs ie.
    #   ...rib/0001/0001.rib
    #   ...rib/0002/0002.rib
    # The second will have the full paths to the xxx_Final ribs ie.
    #   ...rib/0021/perspShape_Final.0021.rib
    # The last list will have the full paths to any geometry ribs and other
    # passes ie.
    #    ...rib/0010/particleShape1.0010.rib
    #    ...rib/0021/rmanDeepShadowPass.0021.rib
    def getRMSFrameRibs(self, layer, scene, project, begin, end):
        scene = os.path.splitext(scene)[0] # Remove .ma/.mb extension
        rootribs =  []
        finalribs = []
        geomribs = []
        pattern = re.compile(r"_Final")

        ribDirPath = os.path.join(project,'renderman', scene,'rib')
        frameDirs = os.listdir(ribDirPath)
        for frameDir in frameDirs:
            if len(frameDir) == 4:
                frame = int(frameDir)
                if frame >= int(begin) and frame <= int(end):
                    # In the case of the default layer the root ribs will be,
                    #     0001.rib, otherwise,
                    #     0001_prman_deepmapshadows.rib
                    # However, if there are more than one layer and the master layer
                    # is selected we get a name such as,
                    #     0003_masterLayer.rib
                    if layer != 'defaultRenderLayer':
                        rootname = frameDir + '_' + layer + '.rib'
                    else:
                        rootname = frameDir + '.rib'
                    rootrib = os.path.join(ribDirPath, frameDir, rootname)
                    if os.path.exists(rootrib) == False and layer == 'defaultRenderLayer':
                        rootname = frameDir + '_masterLayer.rib'
                        rootrib = os.path.join(ribDirPath, frameDir, rootname)
                    #print rootrib

                    frameDir = os.path.join(ribDirPath, frameDir)
                    allribs = os.listdir(frameDir)
                    for rib in allribs:
                        if rib.endswith('.rib') == False:
                            continue
                        rib = os.path.join(frameDir,rib) # full path
                        if rib == rootrib:
                            rootribs.append(rib)
                        elif pattern.search(rib, 1):
                            finalribs.append(rib)
                        else:
                            geomribs.append(rib)    
        return [rootribs, finalribs, geomribs]

    # Utility_____________________________________________
    # Returns the full paths of ribs found in the RMS 'job' directory. 
    # For example,
    #   .../rib/job/nurbsSphereShape1.job.rib
    #   .../rib/job/nurbsSphereShape2.job.rib
    #
    def getRMSJobRibs(self, scene, project):
        scene = os.path.splitext(scene)[0] # Remove .ma/.mb extension
        outList = [ ]
        jobDirPath = os.path.join(project,'renderman', scene,'rib','job')
        jobribs = os.listdir(jobDirPath)
        for rib in jobribs:
            if rib.endswith('.rib') == False:
                continue
            ribpath = os.path.join(jobDirPath, rib)
            outList.append(ribpath)    
        return outList

    # Utility_____________________________________________
    # Writes a file of the following form.
    #    cd /Users/mkesson/Documents/maya/projects/DEEPIMAGE/
    #    prman -t:all renderman/meshToBlobby/rib/0001/0001.rib
    #    prman -t:all renderman/meshToBlobby/rib/0002/0002.rib
    #     ditto...
    #
    def makeBatchRenderScript(self, scene, rootDir, batchPath, ribs, platform,
            begin, end):
        if len(ribs) <= 0: return

        def _pbsSweepJobPath(rib):
            arrstr = '`printf %04d $PBS_ARRAYID`'
            rib = os.path.dirname(rib)
            rib = os.path.dirname(rib)
            rib = os.path.join(rib, arrstr)
            rib = os.path.join(rib, arrstr+'.rib')
            return rib

        pbssweep = ''
        if platform == 'posix':
            pbssweep = Job.convertToLinux(_pbsSweepJobPath(ribs[0]))
        else:
            pbssweep = Job.convertToWindows(_pbsSweepJobPath(ribs[0]))

        f = open(batchPath, 'w')
        f.write('#!/bin/bash\n')
        f.write('#PBS -N ' + scene + '\n')
        f.write('#PBS -l nodes=1:ppn=32\n')
        f.write('#PBS -t ' + str(begin)+'-'+str(end) + '\n')
        f.write('#PBS -q prman\n')
        f.write('cd $PBS_O_WORKDIR\n')
        f.write('prman -t:all ' + pbssweep + '\n')
        f.close()


        # if os.name == "nt":
            # f.write("SET\n")
        # if len(rootDir) > 0:
            # if os.name == "nt":
                # rootDir = Job.convertToWindows(rootDir)
            # f.write("cd " + rootDir + "\n")
        # for rib in ribs:
            # if os.name == "nt":
                # rib = Job.convertToWindows(rib)
            # f.write('prman -t:all ' + rib + "\n")
        # f.close()
        return batchPath

    # Utility_____________________________________________    
    def log(self, logname, logMsg):
        f = open(os.path.join(self.logpath,logname), 'w')
        localtime = time.asctime( time.localtime(time.time()) )
        f.write('Time %s.\n' % localtime)
        f.write(logMsg)
        f.close()        

    # Utility_____________________________________________    
    @staticmethod
    def convertToWindows(linuxpath):
        pattern = re.compile(r"/")
        return pattern.sub(r'\\', linuxpath)

    # Utility_____________________________________________    
    @staticmethod
    def convertToLinux(winpath):
        pattern = re.compile(r"\\")
        return pattern.sub(r'/', winpath)

    # Utility_____________________________________________    
    @staticmethod
    def getImagePath(beautyRib):
        f = open(beautyRib, 'r')
        lines = f.readlines()
        for line in lines:
            if line.strip().startswith("Display "):
                tokens = line.split('"')
                path = tokens[1]
                if path.startswith("+") == False:
                    return path
        f.close()

    # Utility_____________________________________________    
    def isGeometryRif(self, rif):
        members = inspect.getmembers(rif)
        for member in members:
            if member[0] in self.geoMethods and str(member[1]).startswith('<bound method'):
                return True
        return False

    # Utility_____________________________________________    
    def removeEmptyStrs(self, inlist):
        def remove(strn): 
            return len(strn.strip())
        return filter(remove, inlist)

    # Utility_____________________________________________    
    def isNumber(self, arg):
        try:
            float(arg)
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    main()
