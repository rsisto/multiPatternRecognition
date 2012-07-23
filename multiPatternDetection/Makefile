INC_DIR= ../ARToolkit/include
LIB_DIR= ../ARToolkit/lib

LDFLAG=-pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0 -L/usr/X11R6/lib -L/usr/local/lib -L$(LIB_DIR)
LIBS= -lARgsub -lARvideo -lAR -lpthread -lglut -lGLU -lGL -lXi -lX11 -lm -pthread -lgstreamer-0.10 -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lrt -lxml2 -lglib-2.0
CFLAG= -O -pthread -I/usr/include/gstreamer-0.10 -I/usr/include/glib-2.0 -I/usr/lib/i386-linux-gnu/glib-2.0/include -I/usr/include/libxml2 -I/usr/X11R6/include -I$(INC_DIR)


OBJS = object.o
HEADDERS = object.h

all: multiPatternDetection

multiPatternDetection: multiPatternDetection.o $(OBJS)
	cc -o multiPatternDetection multiPatternDetection.o $(OBJS) $(LDFLAG) $(LIBS)

multiPatternDetection.o: multiPatternDetection.c $(HEADDERS)
	cc -c $(CFLAG) multiPatternDetection.c

object.o: object.c $(HEADDERS)
	cc -c $(CFLAG) object.c

clean:
	rm -f *.o
	rm -f multiPatternDetection

allclean:
	rm -f *.o
	rm -f multiPatternDetection
	rm -f Makefile
