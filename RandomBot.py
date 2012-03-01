#!/usr/bin/env python
from random import shuffle
from ants import *
from heapq import heappush, heappop
from math import floor, sqrt

class RandomBot:
    def __init__(self):
        self.paths = {}         # paths for ants

        self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('logFile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)

    def find_view_range(self, current_location, ants):
        """! \brief Plaseaza pe o matrice a hartii ce vede o furnica

            \param Un obiect ants din care extragem informatiile necesare

            \return Matricea hartii cu constantele definite in ants.py in
            conformitate cu ceea ce poate vedea o furnica la un anumit moment 
            de timp
        """

        limits = []

        maxim = int(floor(sqrt(ants.viewradius2)))

        for row in range(-maxim, maxim + 1):
            for col in range(-maxim, maxim + 1):
                crt_radius = row**2 + col**2
                if crt_radius <= ants.viewradius2:
                    limits.append((row % ants.height - ants.height, 
                                 col % ants.width - ants.width))

        ants.viewrange = [[False] * ants.width for row in range(ants.height)]

        for ant in ants.my_ants():
            ant_row, ant_col = ant
            for view_row, view_col in limits:
                ants.viewrange[view_row + ant_row][view_col + ant_col] = True

        crt_row, crt_col = current_location
        
        

        return ants.viewrange[crt_row][crt_col]


    def heuristic_cost_estimate(self, start, goal):
        '''Heuristic give estimated cost to goal'''
        return ants.distance(start[0], start[1], goal[0], goal[1])

    def neighbor_nodes(self, current):
        '''Return all neighbors for a given node'''
        l = []
        l.append((current[0] + 1, current[1]))
        l.append( (current[0] - 1, current[1]))
        l.append((current[0], current[1] + 1))
        l.append((current[0], current[1] - 1))
        return l

    def reconstruct_path(came_from, current_node):
        '''Construct path to target, from the beginning'''
        path = []
        while current_node != None:
            path.insert(0, current_node)
            current_node = came_from[current_node]
        return path

    def Astar(self, start, goal, obstacles):
        '''
        start, goal are tuples of the form (row, col);
        obstacles is a function : (row, col) -> return Bool
        '''
        if (obstacles(start[0], start[1]) or obstacles(goal[0], goal[1])):
            return None

        closedset = {}      # The set of nodes already evaluated.
        openset = [start]   # The set of tentative nodes, to be evaluated.
        came_from = {}      # The map of navigated nodes.
        heap = []

        # Stats for starting node.
        g_score = 0
        h_score = heuristic_cost_estimate(start, goal)
        f_score = g_score + h_score
        came_from[start] = None
        heappush(heap, (f_score, start))    # Use heap to store by f_score.

        while openset != []:
            _, current = heappop(heap)      # (f_score, current)
            if current == goal:
                return reconstruct_path(came_from, goal)
            closedset[current] = True        # True that current is in dict
            for neighbor in neighbor_nodes(current):
                if (obstacles(current[0], current[1]) or
                closedset.__contains__(neighbor)):
                    continue
                if neighbor not in openset:
                    openset += [neighbor]
                    h_score = heuristic_cost_estimate(neighbor, goal)
                    g_score = heuristic_cost_estimate(start, neighbor)
                    f_score = g_score + h_score
                    heappush(heap, (f_score, start))
                    came_from[neighbor] = current
        return None

    def do_turn(self, ants):
        destinations = []
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
            if paths.__contains__((a_row, a_col)):
                path = paths.pop((a_row, a_col))    # Get path of this ant
            else:
                closest_food = ants.closest_food(a_row, a_col)
                if closest_food != None:
                    path = Astar((a_row, a_col), closest_food, ants.passable)
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
            (n_row, n_col) = path.pop(0)        # Get next move.
            direction = ants.direction(a_row, a_col, n_row, n_col)
            paths[(n_row, n_col)] = path;       # Update dict of paths.
            ants.issue_order((n_row, n_col, direction))
            destinations.append((n_row, n_col))

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
