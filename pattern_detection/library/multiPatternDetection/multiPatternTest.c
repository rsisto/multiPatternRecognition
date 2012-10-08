#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#include "object.h"
#include "multiPatternDetection.h"

/**
 * Test to multiPatternDetection library. 
 * 
 */

int main(int argc, char **argv)
{

	char objs[] = "";
	int j = arMultiGetIdsMarker(NULL,objs ) ;
	printf("salio test %d\n", j);
	int i;
	sleep(2);
	printf("%s \n",&objs);

	//initialize applications
	arMultiInit(NULL);
	printf("PASO Init\n");

	char c='c';
	int x = 3;
	double z;
	while ((x> 0))  
	{
       c= getchar();
		z = arMultiMarkerTrigDist("Left");
		// arMultiIsMarkerPresent("NotEnter");
		if(z == -1 ){
			printf("ERRORO \n");
		}else{
			printf(" QUAT: Pos x: %3.1f\n",z);
		}

		/*   if(arMultiIsMarkerPresent("NotEnter")==1){
    	  printf("\nHay Kanli");
    	  x= -1;
      }*/
	}

	arMultiCleanup(); 


	return 0;
}
