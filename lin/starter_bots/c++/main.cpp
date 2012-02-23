#include <iostream>

#include "Logging.h"
#include "Bot.h"

int main(int argc, char *argv[])
{
  std::cout.sync_with_stdio(0); 

  Bot* bot = new Bot();
  bot->playGame();
  delete bot;

  LOG("Bot gracefully shutting down...");

  return 0;
}
