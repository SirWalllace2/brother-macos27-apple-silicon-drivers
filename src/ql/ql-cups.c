#include <sys/time.h>
#include <cups/ppd.h>
#define main ptouch_cli_main
#include "../../vendor/ptouch/rastertoptch.c"
#undef main
int main(int argc,char **argv){
 if(argc!=6 && argc!=7){fprintf(stderr,"Usage: rastertoql720 job user title copies options [file]\n");return 1;}
 int copies=atoi(argv[4]);if(copies<1||copies>999)return 1;
 progname="rastertoql720";
 int input=argc==7?open(argv[6],O_RDONLY):0;if(input<0){perror("input");return 1;}
 FILE *spool=tmpfile();if(!spool){perror("spool");return 1;}
 unsigned char buf[65536];ssize_t n;while((n=read(input,buf,sizeof(buf)))>0){if(fwrite(buf,1,n,spool)!=(size_t)n)return 1;}if(n<0)return 1;if(input)close(input);fflush(spool);
 const char *base="QL=true BytesPerLine=90 PixelXfer=ULP Align=Right LabelPreamble=true LastPageFlag=true TransferMode=1 AutoCut=true ChainPrinting=false StatusNotification=0 MinMargin=3 MediaType=Tape";
 cups_option_t *opts=NULL;int count=cupsParseOptions(base,0,&opts);
 ppd_file_t *ppd=NULL;const char *path=getenv("PPD");if(path)ppd=ppdOpenFile(path);
 if(ppd){ppdMarkDefaults(ppd);for(const char **p=(const char*[]){"MediaType","AutoCut",NULL};*p;p++){ppd_choice_t *ch=ppdFindMarkedChoice(ppd,*p);if(ch)count=cupsAddOption(*p,ch->choice,count,&opts);}}
 cups_option_t *user=NULL;int uc=cupsParseOptions(argv[5],0,&user);
 for(const char **k=(const char*[]){"MediaType","AutoCut","MirrorPrint","PrintQuality",NULL};*k;k++){const char *v=cupsGetOption(*k,uc,user);if(v)count=cupsAddOption(*k,v,count,&opts);}
 cupsFreeOptions(uc,user);
 char options[8192]="";size_t used=0;for(int i=0;i<count;i++){int added=snprintf(options+used,sizeof(options)-used,"%s=%s ",opts[i].name,opts[i].value);if(added<0||(size_t)added>=sizeof(options)-used)return 1;used+=added;}
 if(ppd)ppdClose(ppd);cupsFreeOptions(count,opts);
 for(int c=0;c<copies;c++){if(lseek(fileno(spool),0,SEEK_SET)<0)return 1;dup2(fileno(spool),0);job_options_t job=parse_job_options(options);process_rasterdata(&job);if(ferror(stdout))return 1;}
 fclose(spool);return 0;
}
