#include <stdio.h>

#include "Logging.h"
#include "State.h"

void endTurn(State* state)
{
  LOG("Sending endTurn()");

  /* If this wasn't the start game, reset the board. */
  if(state->currentTurnNumber > 0) {
      reset_State(state);
  }

  /* Move to next turn. */
  state->currentTurnNumber++;

  fprintf(stdout, "go\n");
  fflush(stdout);
}

void makeMoves(State* state)
{
  int ant;
  int direction;
  Location newLocation;
  for (ant = 0; ant < state->myAnts.size; ++ant) {
    /* Try moving this ant in some random direction. */
    Location antLocation = state->myAnts.mem[ant];
	direction = rand() % 4;
    newLocation = move(state->myAnts.mem[ant], direction);	
    /* Destination shouldn't be water and shouldn't be an ant. */
    if (!state->grid[newLocation.row][newLocation.column].isWater &&
        state->grid[newLocation.row][newLocation.column].antPlayer == -1) {
      /* Move ant. */
      state->grid[newLocation.row][newLocation.column].antPlayer = 0;
      state->grid[antLocation.row][antLocation.column].antPlayer = -1;
      /* Outputs move information correctly to the engine. */
      fprintf(stdout, "o %d %d %c\n",
              state->myAnts.mem[ant].row,
              state->myAnts.mem[ant].column,
              DIRECTION_LETTER[direction]);
    }
  }
}

void playGame(State* state)
{
  /* Reads in game parameters. */
  LOG("Reading initial parameters.");
  read_State(state);
  endTurn(state);
  LOG("Initial parameters read successfully!");

  srand((unsigned int)seed);

  /* Continues to make moves until game is over. */
  while(read_State(state)) {
    LOG("turn %d:", state->currentTurnNumber);

    mark_visible(state);
    makeMoves(state);

    endTurn(state);
    LOG("Time taken: %lfms\n", getTime(&(state->timer)));
  }
}

int main(int argc, char *argv[])
{
  State state;
  logFile = fopen("logFile.out", "w");

  /** Current state of the game. */
  init_State(&state);
  LOG("State initialized!");

  playGame(&state);

  LOG("Bot gracefully shutting down...");
  
  return 0;
}


