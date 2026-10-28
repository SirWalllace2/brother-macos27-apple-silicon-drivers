#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sane/sane.h>
static void check(SANE_Status s,const char *step){if(s){fprintf(stderr,"%s failed: %d\n",step,s);exit(1);}}
int main(int argc,char **argv){
 if(argc!=4){fprintf(stderr,"Usage: dcp-scan output.pnm dpi gray|color\n");return 2;}
 const SANE_Device **ds;SANE_Handle h;SANE_Int ver,info;SANE_Parameters p;
 check(sane_init(&ver,0),"init");check(sane_get_devices(&ds,1),"devices");
 int n=0;for(;ds[n] && strcmp(ds[n]->model,"DCP-7055");n++);
 if(!ds[n]){fprintf(stderr,"DCP-7055 not found\n");sane_exit();return 1;}
 check(sane_open(ds[n]->name,&h),"open");
 int dpi=atoi(argv[2]); int color=!strcmp(argv[3],"color");
 if((dpi!=100&&dpi!=150&&dpi!=200&&dpi!=300&&dpi!=400&&dpi!=600)||(!color&&strcmp(argv[3],"gray"))){sane_close(h);sane_exit();return 2;}
 char mode[30];strcpy(mode,color?"24bit Color":"True Gray");check(sane_control_option(h,2,SANE_ACTION_SET_VALUE,mode,&info),"mode");
 SANE_Word res=dpi;check(sane_control_option(h,3,SANE_ACTION_SET_VALUE,&res,&info),"resolution");
 SANE_Word x=SANE_FIX(210),y=SANE_FIX(290.9);
 check(sane_control_option(h,10,SANE_ACTION_SET_VALUE,&x,&info),"width");
 check(sane_control_option(h,11,SANE_ACTION_SET_VALUE,&y,&info),"height");
 check(sane_start(h),"start");check(sane_get_parameters(h,&p),"parameters");
 fprintf(stderr,"pixels=%d lines=%d depth=%d format=%d bytes_per_line=%d\n",p.pixels_per_line,p.lines,p.depth,p.format,p.bytes_per_line);
 if(p.format!=(color?SANE_FRAME_RGB:SANE_FRAME_GRAY)||p.depth!=8||p.lines<=0){sane_cancel(h);sane_close(h);sane_exit();return 3;}
 FILE *f=fopen(argv[1],"wb");if(!f){perror("output");sane_cancel(h);sane_close(h);sane_exit();return 4;}
 fprintf(f,"%s\n%d %d\n255\n",color?"P6":"P5",p.pixels_per_line,p.lines);
 unsigned char buf[65536];SANE_Int len=0;SANE_Status s;long total=0;
 while((s=sane_read(h,buf,sizeof(buf),&len))==SANE_STATUS_GOOD){fwrite(buf,1,len,f);total+=len;}
 if(len>0){fwrite(buf,1,len,f);total+=len;}
 fclose(f);fprintf(stderr,"status=%d bytes=%ld expected=%ld\n",s,total,(long)p.bytes_per_line*p.lines);
 sane_cancel(h);sane_close(h);sane_exit();
 return s==SANE_STATUS_EOF && total==(long)p.bytes_per_line*p.lines?0:5;
}
