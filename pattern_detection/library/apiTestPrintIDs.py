"""
  Loads the C api and prints the ids of the markers defined in object_data file. 
"""

import multiPatternDetectionAPI


det = multiPatternDetectionAPI.detection()
salida = det.arMultiGetIdsMarker()
print salida
print salida.split(";")
