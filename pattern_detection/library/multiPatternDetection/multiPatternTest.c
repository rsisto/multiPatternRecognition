#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

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
	
	 printf("%s \n",&objs);
	 /*  for( i= 0; objs[ i ] != '\0'; i++) {
	         printf("%c", objs[ i ]);
	 }  */
	  printf("termino test\n");
	 
  //initialize applications
 /* arMultiInit(NULL);
  printf("PASO Init\n");
  
  char c;
  
  while (1)
    {
      c = getchar();
      if(c== 'x')
        {
          arMultiCleanup();
          exit(0);
        }
      arMultiRefresh();
     printf("/n%d",arMultiIsMarkerPresent("Hiro"));

    }

  return 0;*/
}
