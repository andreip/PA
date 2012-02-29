#!/usr/bin/env python
from random import shuffle
from ants import *
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
        x = ants.distance(int(start[0]), int(start[1]), int(goal[0]), int(goal[1]))
        return x

    def neighbor_nodes(self, current, ants):
        '''Return all neighbors for a given node'''
        l = []
        l.append(((current[0] + 1)%ants.height , current[1]))
        l.append(((current[0] - 1)%ants.height, current[1]))
        l.append((current[0], (current[1] + 1)%ants.width))
        l.append((current[0], (current[1] - 1)%ants.width))
        return l

    def reconstruct_path(self, came_from, current_node):
        '''Construct path to target, from the beginning'''
        path = []
        while came_from[current_node] != None:
            path.insert(0, current_node)
            current_node = came_from[current_node]
        return path

    def Astar(self, start, goal, ants):
        '''
        start, goal are tuples of the form (row, col);
        obstacles is a function : (row, col) -> return Bool
        '''
        if (not ants.passable(start[0], start[1]) or not ants.passable(goal[0], goal[1])):
            return None

        closedset = {}      # The set of nodes already evaluated.
        openset = [start]   # The set of tentative nodes, to be evaluated.
        came_from = {}      # The map of navigated nodes.
        heap = []
        # Stats for starting node.
        g_score = 0
        h_score = self.heuristic_cost_estimate(start, goal,ants)
        f_score = g_score + h_score

        came_from[start] = None
        heappush(heap, (f_score, start))    # Use heap to store by f_score.

        while openset != [] and heap != []:
            _, current = heappop(heap)
            if current == goal:
                return self.reconstruct_path(came_from, goal)
            closedset[current] = True       # True that current is in dict
            
            for neighbor in self.neighbor_nodes(current, ants):
                if (not ants.passable(neighbor[0], neighbor[1]) or
                    closedset.__contains__(neighbor)):
                    continue
                if neighbor not in openset:
                    openset += [neighbor]
                    h_score = self.heuristic_cost_estimate(neighbor,goal,ants)
                    g_score = self.heuristic_cost_estimate(start,neighbor,ants)
                    f_score = g_score + h_score
                    heappush(heap, (f_score, neighbor))
                    came_from[neighbor] = current
        return None

    def do_turn(self, ants):
        destinations = []
        path = []
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
            if self.paths.__contains__((a_row, a_col)):
                path = self.paths.pop((a_row, a_col))    # Get path of this ant
            else:
                closest_food = ants.closest_food(a_row, a_col)
                if closest_food != None:
                    path = self.Astar((a_row, a_col), closest_food, ants)
                # Try all directions randomly until one is passable and not
                # occupied.
                else:
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
        if path != []:
            (n_row, n_col) = path.pop(0)        # Get next move.
            direction = ants.direction(a_row, a_col, n_row, n_col)
            if(not (n_row, n_col) in destinations):
                self.paths[(n_row, n_col)] = path;       # Update dict of paths.
                ants.issue_order((a_row, a_col, direction[0]))
                destinations.append((n_row, n_col))
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
