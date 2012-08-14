import multiPatternDetectionAPI


det = multiPatternDetectionAPI.detection()
salida = det.arMultiGetIdsMarker()
print salida
print salida.split(";")
#det.init()
#while 1:
#  det.refresh()
#  print det.isMarkerPresent("Hiro")
