#!/usr/bin/env python
from random import shuffle
from ants import *
from logging import *
from logutils import *

class RandomBot:

    def __init__(self):
	# for logging
        self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('logFile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)
    
    def do_turn(self, ants):

        self.logger.info("Strating game")
        destinations = []
        for a_row, a_col in ants.my_ants():
            # try all directions randomly until one is passable and not occupied
            directions = AIM.keys()
            self.logger.info("I am loooooping, coaieeeee")
            shuffle(directions)
            for direction in directions:
                self.logger.info("Ana are mere, pere si prune")
                (n_row, n_col) = ants.destination(a_row, a_col, direction)
                if (not (n_row, n_col) in destinations and
                        ants.passable(n_row, n_col)):
                    ants.issue_order((a_row, a_col, direction))
                    destinations.append((n_row, n_col))
                    break
            else:
                destinations.append((a_row, a_col))

if __name__ == '__main__':
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    try:
        Ants.run(RandomBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
