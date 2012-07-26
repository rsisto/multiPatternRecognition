#ifndef MULTIPATTERNDETECTION_H
#define MULTIPATTERNDETECTION_H


//Initializes the library
void arMultiInit();

//Take a screenshot and update the data
void arMultiRefresh();

//Return the data for a specified object
ObjectData_T  *arMultiGetObjectData( char *name );

//Cleanup data and library, release camera
void arMultiCleanup();

int arMultiIsMarkerPresent(char *id);

#endif
