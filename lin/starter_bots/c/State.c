#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "State.h"

Location make_Location(int row, int column) {
  Location location;
  location.row = row;
  location.column = column;
  return location;
}

Location move(Location loc, int dir) {
  Location returnValue = make_Location(
      loc.row + ROW_DIRECTION[dir],
      loc.column + COLUMN_DIRECTION[dir]);

  if (returnValue.row < 0) {
    returnValue.row += mapRows;
  } else if (returnValue.row == mapRows) {
    returnValue.row = 0;
  }

  if (returnValue.column < 0) {
    returnValue.column += mapColumns;
  } else if (returnValue.column == mapColumns) {
    returnValue.column = 0;
  }

  return returnValue;
}

double distance(const Location loc1, const Location loc2)
{
  int d11 = loc1.row - loc2.row;
  int d1 = d11 < 0 ? -d11 : d11;
  int d22 = loc1.column - loc2.column;
  int d2 = d22 < 0 ? -d22 : d22;
  int dr = d1 < (mapRows - d1) ? d1 : (mapRows - d1);
  int dc = d2 < (mapColumns - d2) ? d2 : (mapColumns - d2);
  return dr*dr + dc*dc;
}

void init_Location_vector(Location_vector* lv)
{
  lv->capacity = 0;
  lv->mem = NULL;
  lv->size = 0;
}

void add_Location_vector(Location_vector* lv, Location location)
{
  /* Aloca sau realoca, dupa caz. */
  if (lv->mem == NULL) {
    lv->mem = malloc(100 * sizeof(Location));
    lv->capacity = 100;
  } else if (lv->size == lv->capacity) {
    lv->capacity += 100;
    lv->mem = realloc(lv->mem, lv->capacity * sizeof(Location));
  }

  /* Adauga. */
  lv->mem[lv->size] = location;
  lv->size += 1;
}

void clear_Location_vector(Location_vector* lv)
{
  lv->capacity = 0;
  if (lv->mem != NULL) {
    free(lv->mem);
  }
  lv->mem = NULL;
  lv->size = 0;
}

void init_Square(Square* square)
{
  square->isVisible = false;
  square->isWater = false;
  square->isHill = false;
  square->isFood = false;
  square->hillPlayer = -1;
  square->antPlayer = -1;
}

void reset_Square(Square* square)
{
  square->isVisible = false;
  square->isHill = false;
  square->isFood = false;
  square->hillPlayer = -1;
  square->antPlayer = -1;
}

void init_State(State* state)
{
  int i, j;
  init_Location_vector(&(state->myAnts));
  init_Location_vector(&(state->enemyAnts));
  init_Location_vector(&(state->myHills));
  init_Location_vector(&(state->enemyHills));
  init_Location_vector(&(state->food));

  state->gameOver = false;
  state->currentTurnNumber = 0;

  state->grid = malloc(MAXIMUM_MAP_SIZE * sizeof(Square*));
  for (i = 0; i < MAXIMUM_MAP_SIZE; ++i) {
    state->grid[i] = malloc(MAXIMUM_MAP_SIZE * sizeof(Square));
    for (j = 0; j < MAXIMUM_MAP_SIZE; ++j) {
      init_Square(&(state->grid[i][j]));
    }
  }
}

void reset_State(State* state)
{
  int row, col;
  clear_Location_vector(&(state->myAnts));
  clear_Location_vector(&(state->myHills));
  clear_Location_vector(&(state->enemyAnts));
  clear_Location_vector(&(state->enemyHills));
  clear_Location_vector(&(state->food));

  for(row = 0; row < mapRows; row++) {
    for(col = 0; col < mapColumns; col++) {
        reset_Square(&(state->grid[row][col]));
    }
  }
}

void mark_visible(State* state)
{
  int row, col, ant;
  for (row = 0; row < mapRows; ++row) { 
    for (col = 0; col < mapColumns; ++col) {
      /* Check of any of the ants sees this. */
      for (ant = 0; ant < state->myAnts.size; ++ant) {
        if (distance(make_Location(row, col), state->myAnts.mem[ant]) <= viewRadius) {
          state->grid[row][col].isVisible = true;
          break;
        }
      }
    }
  }
}

/* Input functions. */
int read_State(State* state)
{
  int row, col, player;
  char inputType[256], junk[256];

  /* Read in input type. */
  while(scanf("%s", inputType)) {
    if(strcmp(inputType, "end") == 0) {
      state->gameOver = true;
      break;
    } else if(strcmp(inputType, "turn") == 0) {
      if (!scanf("%d", &(state->currentTurnNumber))) { return false; }
      break;
    } else {
      if (!fgets(junk, 256, stdin)) { return false; }
    }
  }

  if(state->currentTurnNumber == 0) {
    /* If we are at the beginning of the game, read in the parameters. */
    while(scanf("%s", inputType) == 1) {
      if(strcmp(inputType, "loadtime") == 0) {
        if (!scanf("%lf", &loadTime)) { return false; }
      } else if(strcmp(inputType, "turntime") == 0) {
        if (!scanf("%lf", &turnTime)) { return false; }
      } else if(strcmp(inputType, "rows") == 0) {
        if (!scanf("%d", &mapRows)) { return false; }
      } else if(strcmp(inputType, "cols") == 0) {
        if (!scanf("%d", &mapColumns)) { return false; }
      } else if(strcmp(inputType, "turns") == 0) {
        if (!scanf("%d", &totalTurnsNumber)) { return false; }
      } else if(strcmp(inputType, "player_seed") == 0) {
        if (!scanf("%lld", &seed)) { return false; }
        srand((unsigned int)seed);
      } else if(strcmp(inputType, "viewradius2") == 0) {
        if (!scanf("%lf", &viewRadius)) { return false; }
      } else if(strcmp(inputType, "attackradius2") == 0) {
        if (!scanf("%lf", &attackRadius)) { return false; }
      } else if(strcmp(inputType, "spawnradius2") == 0) {
        if (!scanf("%lf", &spawnRadius)) { return false; }
      } else if(strcmp(inputType, "ready") == 0) {
        /* This is the end of the parameter input. */
        start_Timer(&(state->timer));
        break;
      } else {
        if (!fgets(junk, 256, stdin)) { return false; }
      }
    }
  } else {
    /* Reads in information about the current turn. */
    while(scanf("%s", inputType) == 1) {
      if(strcmp(inputType, "w") == 0) {
        /* Water square. */
        if (!(scanf("%d%d", &row, &col) == 2)) { return false; }
        state->grid[row][col].isWater = true;
      } else if(strcmp(inputType, "f") == 0) {
        /* Food square. */
        if (!(scanf("%d%d", &row, &col) == 2)) { return false; }
        state->grid[row][col].isFood = true;
        add_Location_vector(&(state->food), make_Location(row, col));
      } else if(strcmp(inputType, "a") == 0) {
        /* Live ant square. */
        if (!(scanf("%d%d%d", &row, &col, &player) == 3)) { return false; }
        state->grid[row][col].antPlayer = player;
        if(player == 0) {
          add_Location_vector(&(state->myAnts), make_Location(row, col));
        } else {
          add_Location_vector(&(state->enemyAnts), make_Location(row, col));
        }
      } else if(strcmp(inputType, "d") == 0) {
        /* Dead ant squares. */
        if (!(scanf("%d%d%d", &row, &col, &player) == 3)) { return false; }
      } else if(strcmp(inputType, "h") == 0) {
        /* Hill square. */
        if (!(scanf("%d%d%d", &row, &col, &player) == 3)) { return false; }
        state->grid[row][col].isHill = true;
        state->grid[row][col].hillPlayer = player;
        if(player == 0) {
          add_Location_vector(&(state->myHills), make_Location(row, col));
        } else {
          add_Location_vector(&(state->enemyHills), make_Location(row, col));
        }
      } else if(strcmp(inputType, "players") == 0) {
        /* Information about the players. */
        if (!scanf("%d", &numberPlayers)) { return false; }
      } else if(strcmp(inputType, "scores") == 0) {
        /* Information about the scores. */
        int p;
        for(p = 0; p < numberPlayers; ++p) {
          if (!scanf("%lf", &(state->scores[p]))) { return false; }
        }
      } else if(strcmp(inputType, "go") == 0) {
        /* Finished input. */
        if(state->gameOver) {
          LOG("Received end of game message.");
          return false;
        } else {
          start_Timer(&(state->timer));
        }
        break;
      } else {
        if (!fgets(junk, 256, stdin)) { return false; }
      }
    }
  }

  return true;
}


