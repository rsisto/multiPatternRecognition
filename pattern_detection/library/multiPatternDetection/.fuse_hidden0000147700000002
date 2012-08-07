# Runs the multiPatternDetection library
# Every time enter is pressed, an image is captured and the seen objects are logged.
# Entering 'x' and enter quits the program.
export ARTOOLKIT_CONFIG="v4l2src device=/dev/video0 use-fixed-fps=false ! ffmpegcolorspace ! capsfilter caps=video/x-raw-rgb,bpp=24 ! identity name=artoolkit ! fakesink"
./multiPatternDetection

