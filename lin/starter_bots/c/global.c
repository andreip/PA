#ifndef GPARAM_H_
#define GPARAM_H_

#include <stdint.h>
#include <stdio.h>

#ifndef LOGFILENAME
#define LOGFILENAME "logFile.log"
#endif

int mapRows;
int mapColumns;

int numberPlayers;

int64_t seed;

int totalTurnsNumber;

double attackRadius;
double spawnRadius;
double viewRadius;

double loadTime;
double turnTime;

FILE* logFile;

const char DIRECTION_LETTER[4] = { 'N', 'E', 'S', 'W' };

const int ROW_DIRECTION[4] = { -1, 0, 1, 0 };
const int COLUMN_DIRECTION[4] = { 0, 1, 0, -1 };

#endif

