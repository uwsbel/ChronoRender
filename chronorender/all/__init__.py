# import sys, os, inspect

# currpath = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
# paths = [currpath]
# for path in paths:
    # if path not in sys.path:
        # sys.path.insert(0, path)

# from cr import ChronoRender
import chronorender.cr_info as cr_info

if cr_info.cr_light:
    from chronorender.light.cr import ChronoRender
else:
    from cr import ChronoRender

