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
#include <assert.h>
#include <math.h>

/* Object Data */
//Path to the Data folder containing object_data and camera_para.dat files
char *data_path = "Data" ;
char            *model_name = "object_data";
ObjectData_T    *object;
int             objectnum;

int xsize, ysize;
int	thresh = 80;
int count = 0;

/*Camera refresh times  */
double		last_refresh;
double		refresh_windows = 0.05; //seconds to wait before capturing a new frame

/* set up the video format globals */
char			*vconf = "";
char           *cparam_name    = "camera_para.dat";
ARParam         cparam;

static AR2VideoParamT *gVid = NULL;

/* refresh */
void arMultiRefresh(void) {
	//printf("arMultiRefresh");
	ARUint8         *dataPtr;
	ARMarkerInfo    *marker_info;
	int             marker_num;
	int             i,j,k;

	ar2VideoCapNext(gVid);

	/* grab a video frame */
	if( (dataPtr = (ARUint8 *) ar2VideoGetImage(gVid)) == NULL ) {
		printf("arVideGetImage returned null \n");
		return;
	}
	//  printf("dataptr %d %d\n",dataPtr,dataPtr[0]);

	if( count == 0 ) arUtilTimerReset();
	count++;


	/* detect the markers in the video frame */
	if(arDetectMarker(dataPtr, thresh,
			&marker_info, &marker_num) < 0 ) {
		printf("error at arDetectMarker\n");
		arMultiCleanup();
		exit(0);
	}
	if (marker_num > 0) {
		// printf("Detecte %d marcas\n",marker_num);
	}
	/* check for known patterns */
	for( i = 0; i < objectnum; i++ ) {
		//printf("i %d\n",i);
		k = -1;
		for( j = 0; j < marker_num; j++ ) {
			// printf("j %d\n",j);
			if( object[i].id == marker_info[j].id) {

				/* found a pattern */

				//argDrawSquare(marker_info[j].vertex,0,0);

				if( k == -1 ) 
					k = j; 
				else 
					if( marker_info[k].cf < marker_info[j].cf ) k = j; //better confidence factor
			}
		}
		if( k == -1 ) {
			object[i].visible = 0;
			continue;
		}


		/* calculate the transform for each marker */
		if( object[i].visible == 0 ) {
			arGetTransMat(&marker_info[k],
					object[i].marker_center, object[i].marker_width,
					object[i].trans);
		} else {
			arGetTransMatCont(&marker_info[k], object[i].trans,
					object[i].marker_center, object[i].marker_width,
					object[i].trans);

		}
		object[i].visible = 1;
		 printf("Objeto visible %s\n", object[i].name);
	}
	last_refresh = arUtilTimer();

}

ObjectData_T  *arMultiGetObjectData( char *name ) {
	double now = arUtilTimer();
	if(now-last_refresh > refresh_windows )  {
		//take a new capture
		// printf("refreshing cam \n");
		arMultiRefresh();
	} 
	int i;
	for( i = 0; i < objectnum; i++ ) {
		if(strcmp(name, object[i].name)==0) { 
			return &object[i];
		}
	}
	return NULL;
}

int arMultiMarkerTrigDist(char *id) {
	double      cam_trans[3][4];  
	double      quat[4], pos[3];
	
	
	//printf("name %s\n", id);
	ObjectData_T *objeto = arMultiGetObjectData(id); 
	if(objeto != NULL) {

		if ( objeto->visible){ 
			if( arUtilMatInv(objeto->trans, cam_trans) < 0 ){
				return -1;
			}else{
				if( arUtilMat2QuatPos(cam_trans, quat, pos) < 0 ){
					return -1;
				}else{
					//printf(" QUAT: Pos x: %3.1f  y: %3.1f  z: %3.1f\n",pos[0], pos[1], pos[2]);

					return (int) sqrt(pow(pos[0],2) + pow(pos[1],2)+pow(pos[2],2));
				}
			}
		}else{
			return -1;
		}
 
	} else {
		// dio error
		printf("arMultiMarkerTrigDist - undefined id\n");
		return -2;
	}
}


int arMultiIsMarkerPresent(char *id) {


	ObjectData_T *objeto = arMultiGetObjectData(id); 
	if(objeto != NULL) {

		return  objeto->visible ; 
	} else {
		// dio error
		printf("arMultiIsMarkerPresent - undefined id\n");
		return -1;
	}


}

/**
 * Reads the name of the objects defined in object_data
 * puts the names of the ids concatenated with ';' in the output buffer.
 * returns 1 if ok, 0 if no object is read.
 * 
 */ 
int arMultiGetIdsMarker( char* _data_path,char* output) {
	if((_data_path != NULL)) {
		data_path = _data_path;
	}
	Id_Object * obj =  get_ObjDataIds(data_path,model_name);
	if (obj->cant_objects > 0) {
		strcpy(output,"");
		int i;
		for(i=0; i < obj->cant_objects; i++) {
			printf("loaded %s objects \n",obj->objects[i]);
			if(strcmp(output,"")!=0) {
				strcat(output,";");
			}
			strcat(output,obj->objects[i]);

		}
		return 1;
	} else {
		return 0;
	}

}

void arMultiInit( char* _data_path ) {
	ARParam  wparam;
	if(_data_path != NULL) {
		data_path = _data_path;
	}

	/* open the video path */
	gVid = ar2VideoOpen( vconf );
	if( gVid == NULL ) {
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
	if( arParamLoad(camdata_path, 1, &wparam) < 0 ) {
		printf("Camera parameter load error !!\n");
		exit(0);
	}
	arParamChangeSize( &wparam, xsize, ysize, &cparam );
	arInitCparam( &cparam );
	printf("*** Camera Parameter ***\n");
	arParamDisp( &cparam );

	/* load in the object data - trained markers and associated bitmap files */
	//Only if object is null, else duplicate ids of the same objects will be loaded.
	if(object==NULL)
		if( (object=read_ObjData(data_path,model_name, &objectnum)) == NULL ) {
			printf("Error al leer data obj\n");
			exit(0);
		}
	arUtilTimerReset();
	ar2VideoCapStart(gVid);
	last_refresh = arUtilTimer();

}


/* cleanup function called when program exits */
void arMultiCleanup(void) {
	ar2VideoCapStop(gVid);
	ar2VideoClose(gVid);

	free(gVid);
	gVid= NULL;

	argCleanup();
	printf("fin CleanUP");
}
