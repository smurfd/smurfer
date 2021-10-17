#include <stdio.h>
#include <stdlib.h>
#include "cworker.h"

int dowork(int a) {
  int i;
  for(i=0;i<1000;i++) {
    printf("doing hard c-work %d\n", i);
  }
  return i+a;
}

int do_server_work(int a) {
  return a;
}

int do_client_work(int a) {
  return a;
}
