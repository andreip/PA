#!/usr/bin/env python
from random import shuffle
from ants import *
#from math import abs
from heapq import heappush, heappop

class RandomBot:
    def heuristic_cost_estimate(self, start, goal):
        '''Heuristic give estimated cost to goal'''
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

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

    def Astar(self, start, goal):
        '''start, goal are tuples of the form (row, col)'''
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
                if closedset.__contains__(neighbor):
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
            # try all directions randomly until one is passable and not occupied
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
