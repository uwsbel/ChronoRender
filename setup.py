# from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='ChronoRender',
    version='0.1.0',
    author='Aaron Bartholomew',
    author_email='abartholome2@wisc.edu',
    packages=find_packages('chronorender'),
    package_dir={'':'chronorender'},
    url='sbel.wisc.edu/Resources/Software/ChronoEngine/c_render',
    license='LICENSE.txt',
    description='RenderMan Rendering Service Package',
    long_description=open('README.txt').read(),
    scripts=['bin/cmovie.py', 'bin/crender.py', 'bin/crender_sim.py', 'bin/script_utils.py'],
    package_data={
      'chronorender': [
        'cr.conf.yml',
        'assets/*.yml',
        'assets/*.rib',
        'assets/*.sl',
        'assets/shaders/*.sl',
        'assets/textures/*.tif'
      ],
      'chronorender.plugins': [ 
      'plugin_manager.yml',
      'dataprocess/*.py', 
      'datasource/*.py', 
      'distributed/*.py',
      'geometry/*.py', 
      'movie/*.py',
      'renderobject/*.py', 
      'renderpass/*.py'
      ]
      }
    )
