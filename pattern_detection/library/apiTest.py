import multiPatternDetectionAPI

det = multiPatternDetectionAPI.detection()
det.init()
while 1:
  det.refresh()
  print det.isMarkerPresent("Hiro")
