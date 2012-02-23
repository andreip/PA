#ifndef TIMER_H_
#define TIMER_H_

/* Struct for checking how long it has been since the start of the turn. */
#ifdef _WIN32 //Windows timer (DON'T USE THIS TIMER UNLESS YOU'RE ON WINDOWS!)
#include <time.h>
#include <io.h>
#include <windows.h>

typedef struct Timer {
  clock_t startTime, currentTime;
} Timer;

void start_Timer(Timer* timer);
double getTime(Timer* timer);

#else //Mac/Linux Timer
#include <sys/time.h>

typedef struct Timer {
  struct timeval time;
  double startTime, currentTime; 
} Timer;

/* Starts the timer. */
void start_Timer(Timer* timer);
/* How long it has been since the timer was last started in milliseconds. */
double getTime(Timer* timer);

#endif

#endif //TIMER_H_
