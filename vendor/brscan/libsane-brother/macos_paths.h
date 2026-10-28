#ifndef BRSCAN_MACOS_PATHS_H
#define BRSCAN_MACOS_PATHS_H
#include <stdlib.h>
#include <stdio.h>
static inline const char *brscan_path(const char *name) {
 static char paths[8][4096]; static unsigned int slot;
 char *p=paths[(slot++)%8]; const char *base=getenv("BRSCAN_DATA_DIR");
 if(!base)base=".";
 snprintf(p,4096,"%s/%s",base,name);return p;
}
#endif
