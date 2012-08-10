#!/usr/bin/env python
# archivo prueba.py completo

import gtk
import sys, os
import logging
from gettext import gettext as _
from plugins.plugin import Plugin
from TurtleArt.tautils import convert

from TurtleArt.tapalette import make_palette, define_logo_function
from TurtleArt.talogo import primitive_dictionary, logoerror, \
    media_blocks_dictionary
from TurtleArt.taconstants import MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS, \
    EXPAND_SKIN, BLOCKS_WITH_SKIN 
 
import gtk
from time import time
import os.path
from gettext import gettext as _




try:
    from sugar.datastore import datastore
except ImportError:
    pass

from ConfigParser import SafeConfigParser

plugin_name = 'pattern'
plugin_folder = 'pattern_detection'
    
sys.path.insert(0, os.path.abspath('./plugins/'+plugin_folder+'/library'))

import multiPatternDetectionAPI as detectionAPI     

_logger = logging.getLogger('TurtleArt-activity pattern_detection plugin')

class Pattern_detection(Plugin):
   #Detection api class
   detection = None
   
   def __init__(self, parent):
      self._parent = parent
      self._status = False


   def setup(self):
      SKIN_PATHS.append('plugins/'+plugin_folder+'/images')
      palette = make_palette(plugin_name,
                     colors=["#00FF00","#008000"],
                     help_string=_('Esta paleta sigue '))      

      
      primitive_dictionary['isPresent'] = self._isPresent
      palette.add_block('isPresent',
                          style='number-style-1arg',
                          label=_('Viendo Senial'),
                          prim_name='isPresent',
                          help_string= 'Devuelve 1 si la senial esta en el campo visual de la camara')
      self._parent.lc.def_prim('isPresent', 1,
                             lambda self, x: primitive_dictionary['isPresent'](x))
	     
      #TODO: obtener identificadores del api y cargar botones con imágenes.	
      parser = SafeConfigParser()
      found = parser.read(os.path.abspath('./plugins/'+plugin_folder)+'/signals.ini')
      print os.path.abspath('./plugins/'+plugin_folder)
      for section_name in parser.sections():
        print 'Signal found:', section_name
        #image_name= parser.get(section_name, 'imagename')
        label =  parser.get(section_name, 'bottontext')
        self._add_signal_botton(palette,section_name,label)
 
      print '  fin setup'

   def stop(self):
      print 'Stop'

   def quit(self):
      print 'Quit'

   def clear(self):
      print 'Clear'
      pass
   
   def start(self):
      ''' Initialize the camera if there is an camera block in use '''
      #TODO: if len(self._parent.block_list.get_similar_blocks('block',
      #   ['camera', 'read_camera', 'luminance'])) > 0:
      #   if self._camera is None:
      #      self._camera = Camera(self._imagepath)

   def _add_signal_botton(self,palette,block_name,label):    
 
	   palette.add_block(block_name ,
		                  style='box-style-media',
		                  label='',
		                  default=block_name,
		                  prim_name=block_name,
	                  	  help_string= label )

	   BLOCKS_WITH_SKIN.append(block_name)
	   NO_IMPORT.append(block_name)
	   MEDIA_SHAPES.append(block_name + 'off')
	   MEDIA_SHAPES.append(block_name + 'small')
	   EXPAND_SKIN[block_name] = (0, 10)
	   #if expand > 0:
           #  EXPAND_SKIN[block_name] = expand
      	   self._parent.lc.def_prim(block_name , 0, lambda self: block_name)
 
   #TODO: enganchar métodos de api.
   def _isPresent(self,valor):
     print  "el valor del boton "+ valor
     if valor == 'Hiro':
     	return True
     else:
     	return False

#### FIN DEL ARCHIVO #####
