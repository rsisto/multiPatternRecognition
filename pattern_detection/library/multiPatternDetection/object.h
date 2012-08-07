#ifndef OBJECT_H
#define OBJECT_H


#define   OBJECT_MAX       30

typedef struct {
    char       name[256]; //name defined in object_data file
    int        id; // internal id used by ARToolkit
    int        visible; // 1 if visible, 0 if not.
    double     marker_coord[4][2]; //TODO: find out
    double     trans[3][4]; // TOOD: find out
    double     marker_width; // TOOD: find out
    double     marker_center[2]; // TOOD: find out
} ObjectData_T;

ObjectData_T  *read_ObjData(char* data_path, char *name, int *objectnum );

#endif
