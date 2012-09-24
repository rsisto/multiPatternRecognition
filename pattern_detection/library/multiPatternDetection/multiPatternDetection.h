#ifndef MULTIPATTERNDETECTION_H
#define MULTIPATTERNDETECTION_H

#define   OBJECT_MAX       30  //MISMA QUE EN OBJECT.C

//Initializes the library 
//_data_path, path to the object_data and camera_param.dat files
void arMultiInit(char* _data_path );

//Take a screenshot and update the data
void arMultiRefresh();

//Return the data for a specified object
ObjectData_T  *arMultiGetObjectData( char *name );

//int arMultiGetObjectData( char *name );

//Cleanup data and library, release camera
void arMultiCleanup();

// 1 is present, -1 error
int arMultiIsMarkerPresent(char *id);

int arMultiGetIdsMarker( char* _data_path,char* output);

#endif
