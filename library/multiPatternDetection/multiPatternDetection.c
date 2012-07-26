#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#include <AR/gsub.h>
#include <AR/param.h>
#include <AR/ar.h>
#include <AR/video.h>
#include "object.h"
#include "multiPatternDetection.h"

/* Object Data */
char            *model_name = "Data/object_data";
ObjectData_T    *object;
int             objectnum;

int             xsize, ysize;
int		thresh = 100;
int             count = 0;

/*Variable para el tiempo de refresh */
double		last_refresh;

 double		refresh_windows = 0.05;

/* set up the video format globals */

char			*vconf = "";


char           *cparam_name    = "Data/camera_para.dat";
ARParam         cparam;

/* refresh */
void arMultiRefresh(void)
{
  ARUint8         *dataPtr;
  ARMarkerInfo    *marker_info;
  int             marker_num;
  int             i,j,k;
  arVideoCapNext();
  arVideoCapNext();
  arVideoCapNext();
   
  /* grab a video frame */
  if( (dataPtr = (ARUint8 *)arVideoGetImage()) == NULL )
    {
      // arUtilSleep(2);
      return;
    }

  if( count == 0 ) arUtilTimerReset();
  count++;


  /* detect the markers in the video frame */
  if(arDetectMarker(dataPtr, thresh,
                    &marker_info, &marker_num) < 0 )
    {
      arMultiCleanup();
      exit(0);
    }
  if (marker_num > 0)
    {
      //printf("Detecte %d marcas\n",marker_num);
    }
  for( i = 0; i < marker_num; i++ )
    {
      //argDrawSquare(marker_info[i].vertex,0,0);
    }

  /* check for known patterns */
  for( i = 0; i < objectnum; i++ )
    {

      k = -1;
      for( j = 0; j < marker_num; j++ )
        {
          // printf("j %d\n",j);
          if( object[i].id == marker_info[j].id)
            {

              /* you've found a pattern */
              //printf("Found pattern: %d ",object[i].id);
              //glColor3f( 0.0, 1.0, 0.0 );
              //argDrawSquare(marker_info[j].vertex,0,0);

              if( k == -1 ) k = j;
              else /* make sure you have the best pattern (highest confidence factor) */
                // printf("not Found pattern: %d ",object[i].id);
                if( marker_info[k].cf < marker_info[j].cf ) k = j;
            }
        }
      if( k == -1 )
        {
          object[i].visible = 0;
          continue;
        }

      /* calculate the transform for each marker */
      if( object[i].visible == 0 )
        {
          arGetTransMat(&marker_info[k],
                        object[i].marker_center, object[i].marker_width,
                        object[i].trans);
        }
      else
        {
          arGetTransMatCont(&marker_info[k], object[i].trans,
                            object[i].marker_center, object[i].marker_width,
                            object[i].trans);

        }
      object[i].visible = 1;
      printf("Objeto visible %s\n", object[i].name);
      printf("Data : %f %f %f\n", object[i].trans[0][3], object[i].trans[1][3], object[i].trans[2][3]);
    }

  last_refresh = arUtilTimer();
}

ObjectData_T  *arMultiGetObjectData( char *name ){
   double now = arUtilTimer();
   if(now-last_refresh > refresh_windows )  {
	arMultiRefresh();
	}
 int i;
   for( i = 0; i < objectnum; i++ ){
      if(strcmp(name, object[i].name)==0){
        return &object[i];
      }
   }
  return NULL;
}  

int arMultiIsMarkerPresent(char *id){
   ObjectData_T *objeto = arMultiGetObjectData(id);
   if(objeto != NULL){
     return  objeto->visible ;
   }else{
      // dio error
      return -1;
    }
   
}

void arMultiInit( void )
{
  ARParam  wparam;

  /* open the video path */
  if( arVideoOpen( vconf ) < 0 ) exit(0);
  /* find the size of the window */
  if( arVideoInqSize(&xsize, &ysize) < 0 ) exit(0);
  printf("Image size (x,y) = (%d,%d)\n", xsize, ysize);

  /* set the initial camera parameters */
  if( arParamLoad(cparam_name, 1, &wparam) < 0 )
    {
      printf("Camera parameter load error !!\n");
      exit(0);
    }
  arParamChangeSize( &wparam, xsize, ysize, &cparam );
  arInitCparam( &cparam );
  printf("*** Camera Parameter ***\n");
  arParamDisp( &cparam );

  /* load in the object data - trained markers and associated bitmap files */
  if( (object=read_ObjData(model_name, &objectnum)) == NULL )
    {
      printf("Error al leer data obj\n");
      exit(0);
    }
 arUtilTimerReset();
last_refresh = arUtilTimer();
}


/* cleanup function called when program exits */
void arMultiCleanup(void)
{
  arVideoCapStop();
  arVideoClose();
  argCleanup();
}
