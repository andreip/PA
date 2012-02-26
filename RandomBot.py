#!/usr/bin/env python
from random import shuffle
from ants import *
<<<<<<< HEAD
#from math import abs
=======
>>>>>>> 65070d9f4abb6b9cfe71aeab33e1edc755d9d7af
from heapq import heappush, heappop
from logging import *
from logutils import *
from sys import *

class RandomBot:
    def __init__(self):
        self.paths = {}         # paths for ants
	self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('logFile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)

    def heuristic_cost_estimate(self, start, goal,ants):
        '''Heuristic give estimated cost to goal'''
	self.logger.info("Intra in heuristic_estimate")
        x = ants.distance(int(start[0]), int(start[1]), int(goal[0]), int(goal[1]))
	return x

    def neighbor_nodes(self, current):
        '''Return all neighbors for a given node'''
        l = []
        l += (current[0] + 1, current[1])
        l += (current[0] - 1, current[1])
        l += (current[0], current[1] + 1)
        l += (current[0], current[1] - 1)
        return l

    def reconstruct_path(came_from, current_node):
        '''Construct path to target, from the beginning'''
        path = []
        while current_node != None:
            path.insert(0, current_node)
            current_node = came_from[current_node]
        return path

    def Astar(self, start, goal, ants):
        '''
        start, goal are tuples of the form (row, col);
        obstacles is a function : (row, col) -> return Bool
        '''
	self.logger.info("Intra in Astar")
        if (not ants.passable(start[0], start[1]) or not ants.passable(goal[0], goal[1])):
	    self.logger.info("Intra in obstacle test")
	    self.logger.info(start[0])
	    self.logger.info(start[1])
	    self.logger.info(goal[0])
	    self.logger.info(goal[1])
            return None
	
	self.logger.info("Trece de passable test")
        closedset = {}      # The set of nodes already evaluated.
        openset = [start]   # The set of tentative nodes, to be evaluated.
        came_from = {}      # The map of navigated nodes.
        heap = []

	self.logger.info("Ajunge inainte de heuristic_cost")
        # Stats for starting node.
        g_score = 0
        h_score = self.heuristic_cost_estimate(start, goal,ants)
	self.logger.info(h_score)
        f_score = g_score + h_score
        came_from[start] = None
        heappush(heap, (f_score, start))    # Use heap to store by f_score.
	self.logger.info("Ajunge inainte de while")
        while openset != [] and heap != []:
	    self.logger.info("Intra in while")
            _, current = heappop(heap)      # (f_score, current)

	    self.logger.info("Intra inainte de if")
            if current == goal:
		self.logger.info("Intra in if")
                return self.reconstruct_path(came_from, goal)
            closedset[current] = True       # True that current is in dict
	
	    self.logger.info("Ajunge inainte de for")
            for neighbor in self.neighbor_nodes(current):
		self.logger.info("Intra in for")
                if (ants.passable(current[0], current[1]) or
                closedset.__contains__(neighbor)):
		    self.logger.info("Intra in primul if")
                    continue
                if neighbor not in openset:
		    self.logger.info("Intra in al doilea if")
                    openset += [neighbor]
                    h_score = heuristic_cost_estimate(neighbor,goal,ants)
                    g_score = heuristic_cost_estimate(start,neighbor,ants)
		    self.logger.info("Ajunge dupa h si g_score")
                    f_score = g_score + h_score
                    heappush(heap, (f_score, start))
                    came_from[neighbor] = current
		    self.logger.info("Ajunge la finalul if")
	    self.logger.info("Ajunge la finalul for")
	self.logger.info("Ajunge la finalul while")
	self.logger.info("Ajunge la finalul Astar")
        return None

    def do_turn(self, ants):
	self.logger.info("Starting game")
        destinations = []
	path = None
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
	    self.logger.info("I am loooooping, coaieeeee")
            if self.paths.__contains__((a_row, a_col)):
		self.logger.info("A trecut de paths.contains")
                path = self.paths.pop((a_row, a_col))    # Get path of this ant
            else:
		self.logger.info("A trecut de else")
                closest_food = ants.closest_food(a_row, a_col)
                if closest_food != None:
	            self.logger.info("A gasit closest_food")
                    path = self.Astar((a_row, a_col), closest_food, ants)
                # Try all directions randomly until one is passable and not
                # occupied.
		    self.logger.info("A mers Astar")
                else:
	            self.logger.info("A mers pe ramura fara close_food")
                    directions = AIM.keys()
                    shuffle(directions)
                    for direction in directions:
                        (n_row, n_col) = ants.destination(a_row, a_col, direction)
                        if (not (n_row, n_col) in destinations and
                            ants.passable(n_row, n_col)):
                            ants.issue_order((a_row, a_col, direction))
                            destinations.append((n_row, n_col))
                            break
                    else:
                        destinations.append((a_row, a_col))
                    continue
	    
	    self.logger.info("Mergeee")
	    if path != None:
                (n_row, n_col) = path.pop(0)        # Get next move.
	    	self.logger.info(n_row)
	    	self.logger.info(n_col)
            	direction = ants.direction(a_row, a_col, n_row, n_col)
            	self.paths[(n_row, n_col)] = path;       # Update dict of paths.
            	ants.issue_order((n_row, n_col, direction))
            	destinations.append((n_row, n_col))
	    self.logger.info("Ajunge la ultimul for din program")

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
