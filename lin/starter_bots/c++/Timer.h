#ifndef TIMER_H_
#define TIMER_H_

/* Struct for checking how long it has been since the start of the turn. */
#ifdef _WIN32 //Windows timer (DON'T USE THIS TIMER UNLESS YOU'RE ON WINDOWS!)

#include <time.h>
#include <io.h>
#include <windows.h>

struct Timer
{
  clock_t startTime, currentTime;

  void start()
  {
    startTime = clock();
  };

  double getTime()
  {
    currentTime = clock();

    return (double)(currentTime - startTime);
  };
};

#else //Mac/Linux Timer

#include <sys/time.h>
struct Timer
{
  timeval timer;
  double startTime, currentTime;

  /* Starts the timer. */
  void start()
  {
    gettimeofday(&timer, NULL);
    startTime = timer.tv_sec+(timer.tv_usec/1000000.0);
  };

  /* How long it has been since the timer was last started in milliseconds. */
  double getTime()
  {
    gettimeofday(&timer, NULL);
    currentTime = timer.tv_sec+(timer.tv_usec/1000000.0);
    return (currentTime-startTime)*1000.0;
  };
};
#endif


#endif //TIMER_H_
