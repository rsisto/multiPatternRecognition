from ctypes import *

import os

#Library: multiPatternDetectionAPI

#>>> from ctypes import *
#>>> multiPatternLib = cdll.LoadLibrary('./libMultiPatternDetection.so')
#>>> multiPatternLib.arMultiInit()



class detection:
  multiPatternLib = None
  video = None
  
  #Init de la clase robot
  def __init__(self, video = "/dev/video0" ):
    #TODO: falta pasar el directorio de Data como parametro. Si no cuando se hace el init la libreria no encuentra.
    #TODO: pasar video como parametro.
    self.video = video
    os.environ['ARTOOLKIT_CONFIG']= 'v4l2src device='+self.video+' use-fixed-fps=false ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink'
    library_location = os.path.abspath(os.path.join(os.path.dirname(__file__), 'multiPatternDetection/libMultiPatternDetection.so'))
    self.multiPatternLib = cdll.LoadLibrary(library_location)
    #Export the ARTOOLKIT_CONFIG system variable which will be used by artoolkit
    
  
  def init(self):
    data_params = os.path.abspath(os.path.join(os.path.dirname(__file__), 'multiPatternDetection/Data'))
    self.multiPatternLib.arMultiInit(data_params)
  
  def refresh(self):
    self.multiPatternLib.arMultiRefresh()
  
  def cleanup(self):
    self.multiPatternLib.arMultiCleanup()
  
  def isMarkerPresent(self, marker):
    return self.multiPatternLib.arMultiIsMarkerPresent(marker)
  
  
  
