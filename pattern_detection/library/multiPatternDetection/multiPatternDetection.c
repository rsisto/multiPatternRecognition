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
//Path to the Data folder containing object_data and camera_para.dat files
char *data_path = "Data" ;
char            *model_name = "object_data";
ObjectData_T    *object;
int             objectnum;

int xsize, ysize;
int	thresh = 100;
int count = 0;

/*Variable para el tiempo de refresh */
double		last_refresh;
double		refresh_windows = 0.05;

/* set up the video format globals */
char			*vconf = "";
char           *cparam_name    = "camera_para.dat";
ARParam         cparam;

static AR2VideoParamT *gVid = NULL;

/* refresh */
void arMultiRefresh(void)
{
  
  ARUint8         *dataPtr;
  ARMarkerInfo    *marker_info;
  int             marker_num;
  int             i,j,k;
  
  ar2VideoCapNext(gVid);
   
  /* grab a video frame */
  if( (dataPtr = (ARUint8 *) ar2VideoGetImage(gVid)) == NULL )
    {
      // arUtilSleep(2);
      printf("arVideGetImage retorno null \n");
      return;
    }
//  printf("dataptr %d %d\n",dataPtr,dataPtr[0]);
  
  if( count == 0 ) arUtilTimerReset();
  count++;


  /* detect the markers in the video frame */
  if(arDetectMarker(dataPtr, thresh,
                    &marker_info, &marker_num) < 0 )
    {
      printf("error at arDetectMarker\n");
      arMultiCleanup();
      exit(0);
    }
  if (marker_num > 0)
    {
     // printf("Detecte %d marcas\n",marker_num);
    }
  /* check for known patterns */
  for( i = 0; i < objectnum; i++ )
    {
      //printf("i %d\n",i);
      k = -1;
      for( j = 0; j < marker_num; j++ )
        {
          // printf("j %d\n",j);
          if( object[i].id == marker_info[j].id)
            {

              /* you've found a pattern */
              printf("Found pattern: %d ",object[i].id);
              //glColor3f( 0.0, 1.0, 0.0 );
              //argDrawSquare(marker_info[j].vertex,0,0);

              if( k == -1 ) k = j;
              else /* make sure you have the best pattern (highest confidence factor) */
                 printf("not Found pattern: %d ",object[i].id);
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
    //  printf("Data : %f %f %f\n", object[i].trans[0][3], object[i].trans[1][3], object[i].trans[2][3]);
    }
  //object[0].visible=1;
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
      //printf("arMultiIsMarkerPresent - undefined id\n");
      return -1;
    }
    
   
}

char *MyStrdup( const char *str )
{
    char *dup = malloc( strlen( str ) + 1 );
    return dup ? strcpy( dup, str ) : dup;
}

int arMultiGetIdsMarker( char* _data_path,char* output){
	 if((_data_path != NULL)){
	    data_path = _data_path;
	  }	
	 Id_Object * obj =  get_ObjDataIds(data_path,model_name);
	 if (obj->cant_objects>0){
		// char out[256*obj->cant_objects];
		 char out[]="";
		 char vacio[]="";
		// printf("salio \n");
		 int i; 
		 strcpy(out,"");	 
		  for(i=0; i< obj->cant_objects;i++){
			 //printf("%s \n",obj->objects[i]); 
			 if(strcmp(out,"")!=0){
				 strcat(out,";");
			 }
		 
			 strcat(out,obj->objects[i]);
			 //strncpy(out[i],obj->objects[i],256);
			 //out[i]= MyStrdup(obj->objects[i]);
			
		 } 
		  strcpy(output,out);
		 // printf("%s \n",out);
		 return 1;
	 }else{
		 return 0;
	 }
	  
}

void arMultiInit( char* _data_path )
{
  ARParam  wparam;
  if(_data_path != NULL){
    data_path = _data_path;
  }
 
  /* open the video path */
  gVid = ar2VideoOpen( vconf );
 if( gVid == NULL ){
	 printf("problemas con ar2VideoOpen");
	 exit(0);
 }

  /* find the size of the window */
  ar2VideoInqSize(gVid,&xsize, &ysize);
  printf("Image size (x,y) = (%d,%d)\n", xsize, ysize);

  /* set the initial camera parameters */
  char camdata_path [strlen(data_path) + strlen(cparam_name) + 10];
  strcpy(camdata_path,data_path) ; 
  strcat(camdata_path,"/") ;
  strcat(camdata_path,cparam_name);
  printf("path: %s\n",data_path);
  printf("Camera file: %s\n",camdata_path);
  if( arParamLoad(camdata_path, 1, &wparam) < 0 )
    {
      printf("Camera parameter load error !!\n");
      exit(0);
    }
  arParamChangeSize( &wparam, xsize, ysize, &cparam );
  arInitCparam( &cparam );
  printf("*** Camera Parameter ***\n");
  arParamDisp( &cparam );

  /* load in the object data - trained markers and associated bitmap files */
  if( (object=read_ObjData(data_path,model_name, &objectnum)) == NULL )
    {
      printf("Error al leer data obj\n");
      exit(0);
    }
  arUtilTimerReset();
  ar2VideoCapStart(gVid);
  last_refresh = arUtilTimer();
  
}


/*
void arMultiInit( char* _data_path )
{
  ARParam  wparam;
  if(_data_path != NULL){
    data_path = _data_path;
  }
  /* open the video path */
/*  if( arVideoOpen( vconf ) < 0 ) exit(0);
  /* find the size of the window */
/*  if( arVideoInqSize(&xsize, &ysize) < 0 ) exit(0);
  printf("Image size (x,y) = (%d,%d)\n", xsize, ysize);

  /* set the initial camera parameters */
/*  char camdata_path [strlen(data_path) + strlen(cparam_name) + 10];
  strcpy(camdata_path,data_path) ; 
  strcat(camdata_path,"/") ;
  strcat(camdata_path,cparam_name);
  printf("path: %s\n",data_path);
  printf("Camera file: %s\n",camdata_path);
  if( arParamLoad(camdata_path, 1, &wparam) < 0 )
    {
      printf("Camera parameter load error !!\n");
      exit(0);
    }
  arParamChangeSize( &wparam, xsize, ysize, &cparam );
  arInitCparam( &cparam );
  printf("*** Camera Parameter ***\n");
  arParamDisp( &cparam );

  /* load in the object data - trained markers and associated bitmap files */
/*  if( (object=read_ObjData(data_path,model_name, &objectnum)) == NULL )
    {
      printf("Error al leer data obj\n");
      exit(0);
    }
  arUtilTimerReset();
  arVideoCapStart();
  last_refresh = arUtilTimer();
  
}
*/

/* cleanup function called when program exits */
void arMultiCleanup(void)
{
	ar2VideoCapStop(gVid);
	ar2VideoClose(gVid);
	
	/*free(gVid->videoBuffer);
	free(gVid->pipeline);
	free(gVid->probe);*/
	free(gVid);	
	gVid= NULL;
	
    argCleanup();
    printf("fin CleanUP");
}
/*void arMultiCleanup(void)
{
  arVideoCapStop();
  arVideoClose();
  argCleanup();
}*/
