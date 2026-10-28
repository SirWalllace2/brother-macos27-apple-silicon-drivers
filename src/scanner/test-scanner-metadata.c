#include <assert.h>
#include <string.h>
#include "brother_brscan4.h"
static const unsigned char bytes[]={0x82,0x03,0x00,0x01,0x00,0x84,0x80};
static int read_fake(void *ctx,unsigned char *dst,int want){int *pos=ctx;int n=sizeof(bytes)-*pos;if(n>want)n=want;if(n>2)n=2;if(n>0){memcpy(dst,bytes+*pos,n);*pos+=n;}return n;}
int main(void){Brscan4ReadCache cache;int pos=0;unsigned char out[32];brscan4_cache_reset(&cache);int n=brscan4_read_next_record(&cache,read_fake,&pos,out,sizeof(out));assert(n==1&&out[0]==0x80&&pos==sizeof(bytes));return 0;}
