/** Structure that represents an AI in a game. */
#ifndef BOT_H_
#define BOT_H_

#include "State.h"

struct Bot
{
  /** Current state of the game. */
  State state;

  /** Plays a single game of Ants. */
  void playGame();

  /** Moves ants on the board. */
  void makeMoves();

  /** Indicates to the engine that it has made its moves. */
  void endTurn();
};

#endif

