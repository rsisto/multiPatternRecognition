"""
  Loads the C api, 
    prints the ids of the markers defined in object_data file. 
    Queries the api to detect the first defined marker
"""

import multiPatternDetectionAPI

det = multiPatternDetectionAPI.detection()
salida = det.arMultiGetIdsMarker()
markers = salida.split(";")
print "Markers: " + str(markers)
det.init()
while 1:
  #det.refresh()
  if det.isMarkerPresent(markers[0]) == 0:
    print("nada")
  
