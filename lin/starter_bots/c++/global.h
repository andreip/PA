#ifndef GLOBAL_H_
#define GLOBAL_H_

#include <stdint.h>

#include <iostream>
#include <fstream>

/** Global variables go in this namespace. */

namespace gparam {

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
extern std::ofstream logFile;

}

/** Useful constants go below. */

/** Maximum map size. */
const int MAXIMUM_MAP_SIZE = 200;

/** Directionality constants. */
const int NUMBER_DIRECTIONS = 4;
const int NORTH = 0;
const int EAST = 1;
const int SOUTH = 2;
const int WEST = 3;

/** Pretty printing aids. */
const char DIRECTION_LETTER[NUMBER_DIRECTIONS] = { 'N', 'E', 'S', 'W' };

/** Direction vectors. */
const int ROW_DIRECTION[NUMBER_DIRECTIONS] = { -1, 0, 1, 0 };
const int COLUMN_DIRECTION[NUMBER_DIRECTIONS] = { 0, 1, 0, -1 };

#endif

