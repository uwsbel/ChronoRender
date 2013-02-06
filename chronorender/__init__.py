import os.path, cr_info

if cr_info.cr_light:
    # dirname = __path__[0]
    # __path__.insert(0, os.path.join(dirname,"light"))
    from chronorender.light.cr import ChronoRender
else:
    from chronorender.all.cr import ChronoRender
# import sys, os, inspect

# currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
# paths = [currpath]
# for path in paths:
    # if path not in sys.path:
        # sys.path.insert(0, path)
