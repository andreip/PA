/** Structure for storing information abour the current state of the map. */
#ifndef STATE_H_
#define STATE_H_

#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>
#include <stdint.h>

#include "global.h"

#include "Logging.h"
#include "Timer.h"

/** Structure for representing a location on the map. */
struct Location {
  int row;
  int column;

  Location(int row, int column) : row(row), column(column) { }

  Location move(int dir) {
    Location returnValue(row + ROW_DIRECTION[dir],
                         column + COLUMN_DIRECTION[dir]);
    
    if (returnValue.row < 0) {
      returnValue.row += gparam::mapRows;
    } else if (returnValue.row == gparam::mapRows) {
      returnValue.row = 0;
    }

    if (returnValue.column < 0) {
      returnValue.column += gparam::mapColumns;
    } else if (returnValue.column == gparam::mapColumns) {
      returnValue.column = 0;
    }

    return returnValue;
  }
};

/** Struct for representing a square in the grid. */
struct Square
{
    bool isVisible;
    bool isWater;
    bool isHill;
    bool isFood;
    int hillPlayer;
    int antPlayer;

    Square() : isVisible(false), isWater(false), isHill(false), isFood(false)
    {
      hillPlayer = antPlayer = -1;
    }

    /** Resets the information for the square except water information. */
    void reset()
    {
        isVisible = isHill = isFood = false;
        hillPlayer = antPlayer = -1;
    }
};

struct State
{
  /** False while we keep playing. */

  bool gameOver;
  
  int currentTurnNumber;

  /** Score for each of the current players. */
  std::vector<double> scores;

  /** See definition of Square for further details. */
  std::vector<std::vector<Square> > grid;

  std::vector<Location> myAnts;
  std::vector<Location> enemyAnts;
  std::vector<Location> myHills;
  std::vector<Location> enemyHills;
  std::vector<Location> food;

  /** This could have been global, but there you go... */
  Timer timer;

  /** Constructor creates the map proper. */
  State() : gameOver(false), currentTurnNumber(0)
  {
    for (int i = 0; i < MAXIMUM_MAP_SIZE; ++i) {
      grid.push_back(std::vector<Square>(MAXIMUM_MAP_SIZE, Square()));
    }
  }

  /** Clears non-persistent informatin from the grid after a step. */
  void reset();

  /** Marks visible cells. */
  void mark_visible();

  /** This is just square of Euclid distance. */
  double distance(const Location loc1, const Location loc2);

};

/** Method that helps do the IO. */
std::istream& operator>>(std::istream &is, State &state);

#endif

