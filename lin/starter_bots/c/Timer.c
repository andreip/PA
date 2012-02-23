#include <stdlib.h>

#include "Timer.h"

#ifdef _WIN32 
#include <time.h>
#include <io.h>
#include <windows.h>

void start_Timer(Timer* timer)
{
  timer->startTime = clock();
}

double getTime(Timer* timer)
{
    timer->currentTime = clock();
    return (double)(timer->currentTime - timer->startTime);
}

#else

#include <sys/time.h>
void start_Timer(Timer* timer)
{
    gettimeofday(&(timer->time), NULL);
    timer->startTime = timer->time.tv_sec + (timer->time.tv_usec / 1000000.0);
}

double getTime(Timer* timer)
{
  gettimeofday(&(timer->time), NULL);
  timer->currentTime = timer->time.tv_sec + (timer->time.tv_usec / 1000000.0);
  return (timer->currentTime - timer->startTime)*1000.0;
}

#endif


