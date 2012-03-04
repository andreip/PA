#!/usr/bin/env python
from random import shuffle
from ants import *
from heapq import heappush, heappop
from logging import *
from logutils import *
from sys import *

class MyBot:
    """
    ! \brief Botul pentru prima etapa. Foloseste euristica A* 

    	TODO @Andrei - desciere scurta pt algoritm si abordare a problemei
    """
    
    def __init__(self):
        """
        ! \brief Aici se face initializarea jurnalizarii
    	
		Utila pentru debug sau informatii despre desfasurarea jocului
		"""        
        self.paths = {}         # paths for ants
        
        self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('logFile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr) 
        self.logger.setLevel(logging.INFO)

    def heuristic_cost_estimate(self, (row1, col1), (row2, col2), ants):
        """
         ! \brief Obtine estimarea costului euristic.
            \param start - punctul din care pleaca furnica. Este un tuplu de forma (row, col)
            \param goal - puncul la care se doreste sa ajunga furnica. Este un tuplu de forma (row, col)
            \return Distanta euclidiana dintre cele doua puncte
        """
        row1 = row1 % ants.height
        row2 = row2 % ants.height
        col1 = col1 % ants.width
        col2 = col2 % ants.width
        d_col = min(abs(col1 - col2), ants.width - abs(col1 - col2))
        d_row = min(abs(row1 - row2), ants.height - abs(row1 - row2))
        return d_col + d_row
    
    def neighbor_nodes(self, current, ants):
        """
         ! \brief Returneaza toti vecinii nodului curent.

            \param curent - un tuplu de forma (row, col)
            \return Lista continand vecinii nodului
         """
        l = []
        l.append(( (current[0] + 1) % ants.height, current[1] ))
        l.append(( (current[0] - 1) % ants.height, current[1] ))
        l.append(( current[0], (current[1] + 1) % ants.width ))
        l.append(( current[0], (current[1] - 1) % ants.width ))
        return l
    
    def reconstruct_path(self, came_from, current_node):
        """
        ! \brief Construct path to target, from the beginning
            
            TODO @Stana: pana la urma 
            se mai foloseste functia asta la ceva 
            sau o stergem?
        """
        path = []
        while came_from[current_node] != None:
            path.insert(0, current_node)
            current_node = came_from[current_node]
        return path
    
    def Astar(self, start, goal, ants):
        """
        ! \brief Functia de explorare. 
        
        
    	In cadrul acestei functii trebuie ca fiecare furnica sa aiba o anumita
		tinta: sa mearga dupa mancare, sa omoare o furnica adversa etc.
		Fiecare furnica are un punct de start
        
        TODO @toata_lumea: mai scriem ceva aici?

	      \param start - tuplu de forma (row, col)
	      \param goal - tuplu de forma (row, col)
	      \param ants - furnicile botului nostru. E un list comprehension returnat din ants.py
        """
        
        if (not ants.passable(start[0], start[1]) or not
        ants.passable(goal[0], goal[1])):
            return None
    
        closedset = {}      # The set of nodes already evaluated.
        openset = [start]   # The set of tentative nodes, to be evaluated.
        came_from = {}      # The map of navigated nodes.
        heap = []
        # Stats for starting node.
        g_score = 0
        h_score = self.heuristic_cost_estimate(start, goal, ants)
        f_score = g_score + h_score
    
        came_from[start] = None
        heappush(heap, (f_score, start))    # Use heap to store by f_score.
    
        while openset != []:
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
                    h_score = self.heuristic_cost_estimate(neighbor, goal, ants)
                    g_score = self.heuristic_cost_estimate(start, neighbor, ants)
                    f_score = g_score + h_score
                    heappush(heap, (f_score, neighbor))
                    came_from[neighbor] = current
        return None

    def do_turn(self, ants):
        destinations = []
        path = []
        self.logger.info("nu vrea")
        ants.landmap()
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
            if self.paths.__contains__((a_row, a_col)):
                path = self.paths.pop((a_row, a_col))    # Get path of this ant
            else:
                closest_food = ants.closest_food(a_row, a_col)
                
                dist = maxint
                #dist = 0
                
                if closest_food != None:
                    dist = self.heuristic_cost_estimate((a_row, a_col), closest_food,ants)
                self.logger.info((dist,closest_food))

                if closest_food != None and dist <=10:
                   path = self.Astar((a_row, a_col), closest_food, ants)
                # Try all directions randomly until one is passable and not
                # occupied.
                elif dist >= 10:

                    unseen = ants.closest_unseen(a_row, a_col)
                    self.logger.info(unseen)
                
                    path = self.Astar((a_row, a_col),unseen, ants)
                
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
                    if path != []:
                        self.paths[(n_row, n_col)] = path;       # Update dict of paths.
                    ants.issue_order((a_row, a_col, direction[0]))
                    destinations.append((n_row, n_col))
                else:
                    destinations.append((a_row, a_col))
                self.logger.info(path)

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
