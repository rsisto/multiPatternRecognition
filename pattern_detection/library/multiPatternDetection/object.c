/*
** ARToolKit object parsing function
**   - reads in object data from object file in Data/object_data
**
** Format:
** <obj_num>
**

**
** ...
**
**	eg
**
**	#pattern 1
**	Hiro
**	Data/hiroPatt
**	80.0
**	0.0 0.0
**
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <AR/ar.h>
#include "object.h"

static char *get_buff( char *buf, int n, FILE *fp );

/**
 * Reads from the object_data file only the ids of the objects (not the pattern data).
 * 
 */
Id_Object * get_ObjDataIds(char* data_path, char *name) {
  FILE          *fp;
  Id_Object     *object;
  char           buf[256], buf1[256] , buf2[256];
  int            i;
  int  objectnum   ;

  strcpy(buf2,data_path);
  strcat(buf2,"/");
  strcat(buf2,name);

  printf("Opening Data File %s\n",buf2);

  if( (fp=fopen(buf2, "r")) == NULL ) {
    printf("Can't find the file - quitting \n");
    return(0);
  }
  
  //Read the number of objects (first line with a number)
  get_buff(buf, 256, fp);
  if( sscanf(buf, "%d", &objectnum) != 1 ) {
    printf("sscanf  \n");
    fclose(fp);
    return(0);
  }

  object = (Id_Object  *)malloc( sizeof(Id_Object ));
  if( object == NULL ) {
    printf("no malloc \n");
    return(0);
  }
  
  printf("objects read: %d  \n",objectnum);
  object->cant_objects = objectnum ;
  for( i = 0; i < objectnum; i++ ) {
    get_buff(buf, 256, fp);
    if( sscanf(buf, "%s", object->objects[i]) != 1 ) {
      printf("-1  \n");
      fclose(fp);
      free(object);
      return(0);
    }
    //Discard the next 3 lines (information about object -pattern file name, size, center)
    get_buff(buf, 256, fp);
    get_buff(buf, 256, fp);
    get_buff(buf, 256, fp);

  }//for
  fclose(fp);
  return( object );
}



ObjectData_T *read_ObjData(char* data_path, char *name, int *objectnum ) {
  FILE          *fp;
  ObjectData_T  *object;
  char           buf[256], buf1[256] , buf2[256];
  int            i;

  strcpy(buf2,data_path);
  strcat(buf2,"/");
  strcat(buf2,name);

  printf("Opening Data File %s\n",buf2);

  if( (fp=fopen(buf2, "r")) == NULL ) {
    printf("Can't find the file - quitting \n");
    return(0);
  }

  get_buff(buf, 256, fp);
  if( sscanf(buf, "%d", objectnum) != 1 ) {
    printf("sscanf  \n");
    fclose(fp);
    return(0);
  }

  printf("About to load %d Models\n",*objectnum);

  object = (ObjectData_T *)malloc( sizeof(ObjectData_T) * *objectnum );
  if( object == NULL ) return(0);

  for( i = 0; i < *objectnum; i++ ) {
    object[i].visible = 0;

    get_buff(buf, 256, fp);
    if( sscanf(buf, "%s", object[i].name) != 1 ) {
      printf("-1  \n");
      fclose(fp);
      free(object);
      return(0);
    }

    printf("Read in No.%d \n", i+1);
    printf("%s \n",  object[i].name);

    get_buff(buf, 256, fp);
    if( sscanf(buf, "%s", buf1) != 1 ) {
      printf("1 \n");
      fclose(fp);
      free(object);
      return(0);
    }

    printf("%s \n", buf1);
    strcpy(buf2,data_path);
    strcat(buf2,"/");
    strcat(buf2,buf1);
    printf("path: %s\n",buf2);

    if( (object[i].id = arLoadPatt(buf2)) < 0 ) {
      printf("2 \n");
      fclose(fp);
      free(object);
      return(0);
    }

    get_buff(buf, 256, fp);
    printf("%d \n",object[i].id );

    if( sscanf(buf, "%lf", &object[i].marker_width) != 1 ) {
      printf("3 \n");
      fclose(fp);
      free(object);
      return(0);
    }
    printf("%f \n",object[i].marker_width );
    get_buff(buf, 256, fp);


    if( sscanf(buf, "%lf %lf", &object[i].marker_center[0],
               &object[i].marker_center[1]) != 2 ) {

      fclose(fp);
      free(object);
      return(0);
    }
    printf("%f %f\n",object[i].marker_center[0], object[i].marker_center[1] );
  }

  fclose(fp);

  return( object );
}

/**
 *  Reads from a file and returns the first line wich doesn't start with '#' or '\n'
 *
 */
static char *get_buff( char *buf, int n, FILE *fp ) {
  char *ret;

  for(;;) {
    ret = fgets( buf, n, fp );
    if( ret == NULL ) return(NULL);
    if( buf[0] != '\n' && buf[0] != '#' ) return(ret);
  }
}
