/** Structure for storing information abour the current state of the map. */
#ifndef STATE_H_
#define STATE_H_

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "global.h"

#include "Logging.h"
#include "Timer.h"

/** Structure for representing a location on the map. */
typedef struct Location {
  int row;
  int column;
} Location;

/** Creates and initializes a location to a given row and column. */
Location make_Location(int row, int column);
/** Gives a certain neighbour of a location on the wrapped map. */
Location move(Location loc, int dir);
/* Returns the square of Euclid distance between two locations. */
double distance(const Location loc1, const Location loc2);

typedef struct Location_vector {
  int capacity;
  Location* mem;
  int size;
} Location_vector;

/** Initializes a location vector. */
void init_Location_vector(Location_vector* location_vector);
/** Inserts an element into the vector. */
void add_Location_vector(Location_vector* location_vector, Location element);
/** Clears the vector content. */
void clear_Location_vector(Location_vector* location_vector);

/** Struct for representing a square in the grid. */
typedef struct Square {
    int isVisible;
    int isWater;
    int isHill;
    int isFood;
    int hillPlayer;
    int antPlayer;
} Square;

/** Initializes a Square structure. */
void init_Square(Square* square); 
/** Resets the information for the square except water information. */
void reset_Square(Square* square);

typedef struct State
{
  int currentTurnNumber;

  /** Score for each of the current players. */
  double scores[MAXIMUM_MAP_PLAYERS];

  /** False while we keep playing. */
  int gameOver;

  /** See definition of Square for further details. */
  Square** grid;

  Location_vector myAnts;
  Location_vector enemyAnts;
  Location_vector myHills;
  Location_vector enemyHills;
  Location_vector food;

  /** This could have been global, but there you go... */
  Timer timer;

} State;

/** Initializes a state structure. */
void init_State(State* state);
/** Clears non-persistent informatin from the grid after a step. */
void reset_State(State* state);
/** Marks visible cells. */
void mark_visible(State* state);
/** Method that helps do the IO. */
int read_State(State* state);

#endif

