from ctypes import *

import sys, os

#Library: multiPatternDetectionAPI

#>>> from ctypes import *
#>>> multiPatternLib = cdll.LoadLibrary('./libMultiPatternDetection.so')
#>>> multiPatternLib.arMultiInit()



class detection:
  multiPatternLib = None
  video = None
  OBJECT_MAX = 30
  
  #Init de la clase robot
  def __init__(self, video = "/dev/video0" ):
    self.video = video
    os.environ['ARTOOLKIT_CONFIG']= 'v4l2src device='+self.video+' use-fixed-fps=false ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink'
    
    #Load the libglu.so.3, or else ctypes won't find it if it's not installed in the system
    glut_location = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib/libglut.so.3'))
    cdll.LoadLibrary(glut_location)
    
    library_location = os.path.abspath(os.path.join(os.path.dirname(__file__), 'multiPatternDetection/libMultiPatternDetection.so'))
    self.multiPatternLib = cdll.LoadLibrary(library_location)
    
    #self.multiPatternLib.arMultiMarkerTrigDist.restype =c_double
     
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
  
  def getMarkerTrigDist(self, marker):
    return self.multiPatternLib.arMultiMarkerTrigDist(marker)

  
  def arMultiGetIdsMarker(self):
      data_params = os.path.abspath(os.path.join(os.path.dirname(__file__), 'multiPatternDetection/Data'))
      s = create_string_buffer('\000'*256*self.OBJECT_MAX)
       
      exit = self.multiPatternLib.arMultiGetIdsMarker(data_params,s)
      if exit:
          return  s.value 
      else:
          return ""


       
