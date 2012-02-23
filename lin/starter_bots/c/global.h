#ifndef GLOBAL_H_
#define GLOBAL_H_

#include <stdint.h>
#include <stdio.h>

/** Global variables go here. */

/** Number of rows and columns of the map. */
extern int mapRows;
extern int mapColumns;

/** Number of players on the map. */
extern int numberPlayers;

/** Initial seed. */
extern int64_t seed;

/** Number of available turns. */
extern int totalTurnsNumber;

/** Attack constants. */
extern double attackRadius;
extern double spawnRadius;
extern double viewRadius;

/** Time per load and time per turn. */
extern double loadTime;
extern double turnTime;

/** Log file. */
extern FILE* logFile;

/** Useful constants go below. */

#define false 0
#define true 1

/** Maximum map size. */
#define MAXIMUM_MAP_SIZE 200

/** Maximum players on a map. */
#define MAXIMUM_MAP_PLAYERS 10

/** Directionality constants. */
#define NUMBER_DIRECTIONS 4
#define NORTH 0
#define EAST 1
#define SOUTH 2
#define WEST 3

/** Pretty printing aids. */
extern const char DIRECTION_LETTER[4];

/** Direction vectors. */
extern const int ROW_DIRECTION[4];
extern const int COLUMN_DIRECTION[4];

#endif

