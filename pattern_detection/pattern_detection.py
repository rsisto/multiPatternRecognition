#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
import sys, os
import logging

from TurtleArt.tautils import convert
from plugins.plugin import Plugin
from TurtleArt.tapalette import make_palette
from TurtleArt.talogo import primitive_dictionary, logoerror
from TurtleArt.tapalette import special_block_colors
from TurtleArt.tautils import convert 

from TurtleArt.tapalette import make_palette, define_logo_function
from TurtleArt.talogo import primitive_dictionary, logoerror, \
    media_blocks_dictionary
from TurtleArt.taconstants import MEDIA_SHAPES, NO_IMPORT, SKIN_PATHS, \
    EXPAND_SKIN, BLOCKS_WITH_SKIN 

from time import time
import os.path
from gettext import gettext as _

try:
    from sugar.datastore import datastore
except ImportError:
    print "error al importat datastore"
    pass


plugin_name = 'pattern'
plugin_folder = 'pattern_detection'
    
sys.path.insert(0, os.path.abspath('./plugins/'+plugin_folder+'/library'))

import multiPatternDetectionAPI as detectionAPI

_logger = logging.getLogger('TurtleArt-activity pattern_detection plugin')

class Pattern_detection(Plugin):
   #Detection api class
   detection = None
   block_list= []
   isInit = False
   
   def __init__(self, parent): 
      self._parent = parent
      self._status = False
      self.detection = detectionAPI.detection()

   def setup(self): 
      SKIN_PATHS.append('plugins/'+plugin_folder+'/images')
      palette = make_palette(plugin_name,
                     colors=["#00FF00","#008000"],
                     help_string=_('Deteccion de marcas'))      

      
      primitive_dictionary['isPresent'] = self._isPresent
      palette.add_block('isPresent',
                          style='number-style-1arg',
                          label=_('Viendo Señal'),
                          prim_name='isPresent',
                          help_string= _('Devuelve True si la señal esta en el campo visual de la camara'))
      self._parent.lc.def_prim('isPresent', 1,
                             lambda self, x: primitive_dictionary['isPresent'](x))
      
      primitive_dictionary['stopCam'] = self._stop_cam
      palette.add_block('stopCam',
                          style='basic-style',
                          label=_('Parar Camara'),
                          prim_name='stopCam',
                          help_string= _('Apaga la camara'))
      self._parent.lc.def_prim('stopCam', 0, lambda self :
            primitive_dictionary['stopCam']())
  
      
      primitive_dictionary['getMarkerTrigDist'] = self._getMarkerTrigDist
      palette.add_block('getMarkerTrigDist',
                          style='number-style-1arg',
                          label=_('Distancia Señal'),
                          prim_name='getMarkerTrigDist',
                          help_string= _('Devuelve la distancia a la camara en mm'))
      self._parent.lc.def_prim('getMarkerTrigDist', 1,
                             lambda self, x: primitive_dictionary['getMarkerTrigDist'](x))
	  
      #Se agregan los IDs de botones para luego chequear que esten para activar la camara
      self.block_list.append('isPresent')
      self.block_list.append('stopCam')
      self.block_list.append('getMarkerTrigDist')     
      #TODO: Faltaria ver si levnta el objet_data segun el idioma   
      #obtener identificadores del api y cargar botones con imagenes.	
      out = self.detection.arMultiGetIdsMarker()
      
      for section_name in out.split(";"):
        print 'Signal found:', section_name
        self._add_signal_botton(palette,section_name,section_name)
        self.block_list.append(section_name)
      print '  fin setup'

   def stop(self):
      print 'Stop'
      self._stop_cam()

   def quit(self):
      self._stop_cam()

   def clear(self):
      self._stop_cam()
   
   def start(self):
     ''' Initialize the camera if there is a camera block in use '''   
     if (len(self._parent.block_list.get_similar_blocks('block',['isPresent'])) > 0):
         #hay elementos de la paleta en la pantalla
         if not(self.isInit) :
           self.detection.init()
           self.isInit = True
     
   def end(self):
     print("end pattern_detection")
     
   def _stop_cam(self):      
         if self.isInit:
             self.detection.cleanup()
             self.isInit = False
             print  "Apagar cam"     
                 
   def _add_signal_botton(self,palette,block_name,label):    
      
      
      #If icon exists, use it instead of just the label
      iconPath = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images/'+block_name+'off.svg'))
      
      if os.path.exists(iconPath):
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
      else:
        palette.add_block(block_name ,
                      style='box-style',
                      label=block_name,
                      default=block_name,
                      prim_name=block_name,
                   	  help_string= label )
      self._parent.lc.def_prim(block_name , 0, lambda self: block_name)
 
 
   def _isPresent(self,valor):
     if self.isInit:  
         #print  "el valor del boton "+ valor
         if self.detection.isMarkerPresent(valor)==1:
             return True
         else:
     	     return False
     else:
         return False
   def _getMarkerTrigDist(self,valor):
       return self.detection.getMarkerTrigDist(valor)
   


#### FIN DEL ARCHIVO #####