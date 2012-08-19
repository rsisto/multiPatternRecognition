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
	 /*  for( i= 0; objs[ i ] != '\0'; i++) {
	         printf("%c", objs[ i ]);
	 }  */
	  printf("termino test\n");
	 
  //initialize applications
  arMultiInit(NULL);
  printf("PASO Init\n");
  
  char c='c';
  int x = 3;
  //while ((c!= 'x'))
  while ((x> 0))  
  {
      //c = getchar();
     /* if(c== 'x')
        {
          arMultiCleanup();
          exit(0);
        }*/
      arMultiRefresh();
     //printf("\n%d",arMultiIsMarkerPresent("Hiro"));
   /*   x=arMultiIsMarkerPresent("Hiro");
      if(arMultiIsMarkerPresent("Kanji")==1){
    	  printf("\nHay Kanli");
      }*/
      
      sleep(2);
      x = x-1;
    }

  arMultiCleanup();
  
  
  sleep(4);
  
  arMultiInit(NULL);
  printf("PASO Init\n");
  
  c='c';
   x = 0;
  while ((c!= 'x'))
 // while ((x== 0))  
  {
      c = getchar();
     /* if(c== 'x')
        {
          arMultiCleanup();
          exit(0);
        }*/
      arMultiRefresh();
     //printf("\n%d",arMultiIsMarkerPresent("Hiro"));
      x=arMultiIsMarkerPresent("Hiro");
      if(arMultiIsMarkerPresent("Kanji")==1){
    	  printf("\nHay Kanli");
      }
    }
  
  arMultiCleanup();
  
  return 0;
}
