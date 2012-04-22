#!/usr/bin/env python
from random import shuffle
from ants import *
from heapq import heappush, heappop
from logging import *
from logutils import *
from time import time

try:
    from sys import maxint
except ImportError:
    from sys import maxsize as maxint

DEFAULT_FOOD_DISTANCE = 10
DEFAULT_HILL_DISTANCE = 70

class MyBot:
    """! \brief Botul pentru prima etapa, foloseste algoritmul A*.

        Furnicile noastre, exploreaza cu A*, danduli-se o destinatie, care
        poate fi una din urmatoarele momentan: mancare sau teritoriu
        necunoscut. Totodata, salvam detaliile pe care le vad furnicile la un
        moment dat (pamant, mancare).
    """

    def __init__(self):
        """! \brief Initializeaza jurnalizaarea.

            Utila pentru debug sau informatii despre desfasurarea jocului.
        """
        self.paths = {}         # paths for ants

        self.logger = logging.getLogger('myapp')
        hdlr = logging.FileHandler('logFile.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        self.logger.addHandler(hdlr)
        self.logger.setLevel(logging.INFO)
        self.mancare = []
        self.drum_explorare = []
        self.hills = None

    def heuristic_cost_estimate(self, (row1, col1), (row2, col2), ants):
        """! \brief Obtine estimarea costului; e optimista.

            \param start - punctul din care pleaca furnica.
            \param goal - puncul la care se doreste sa ajunga furnica. 
            \return Distanta minima de patratele 
            pe care o parcurge furnica.
        """
        row1 %= ants.height
        row2 %= ants.height
        col1 %= ants.width
        col2 %= ants.width
        d_col = min(abs(col1 - col2), ants.width - abs(col1 - col2))
        d_row = min(abs(row1 - row2), ants.height - abs(row1 - row2))
        return d_col + d_row

    def neighbor_nodes(self, current, ants):
        """! \brief Returneaza toti vecinii nodului curent.

            \param curent - pozitia curenta, de forma (row, col).
            \return Lista continand vecinii nodului.
         """
        l = []
        l.append(( (current[0] + 1) % ants.height, current[1] ))
        l.append(( (current[0] - 1) % ants.height, current[1] ))
        l.append(( current[0], (current[1] + 1) % ants.width ))
        l.append(( current[0], (current[1] - 1) % ants.width ))
        return l

    def reconstruct_path(self, came_from, current_node):
        """! \brief Construieste drumul din parinte in parinte, pana la nodul
        initial (de la sfarsit spre inceput).

            \param current_node - nodul final, unde ajunge calea construita; e
            de forma unui tuplu (row, col).
            \param came_from - contine parintii nodurilor ce formeaza calea
            spre nodul final.
        """
        path = []
        while came_from[current_node] != None:
            path.insert(0, current_node)
            current_node = came_from[current_node]
        return path

    def Astar(self, start, goal, ants):
        """! \brief Intoarce o cale optima de la sursa la destinatie. 
        
                In prezent tine cont si de obstacole, dar trimite
                furnicile doar dupa mancare sau puncte 
                necunoscute

            \param start - punct de start, de forma (row, col).
            \param goal - punct destinatie, de forma (row, col).
            \param ants - obiectul furnici, construit in Ants.run().
        """

        if (not ants.passable(start[0], start[1]) or not
        ants.passable(goal[0], goal[1])):
            return None

        closedset = {}      # The dict of nodes already evaluated.
        openset = [start]   # The list of tentative nodes, to be evaluated.
        came_from = {}      # The dict of navigated nodes.
        heap = []
        # Stats for starting node.
        g_score = 0
        h_score = self.heuristic_cost_estimate(start, goal, ants)
        f_score = g_score + h_score
        stop_ceas = 0
        alarm = 0
        turntime = ants.turntime * 10**(-3)

        came_from[start] = None
        heappush(heap, (f_score, start))    # Use heap to store by f_score.

        start_ceas = time()

        while openset != []:
            _, current = heappop(heap)
            if current == goal:
                return self.reconstruct_path(came_from, goal)
            closedset[current] = True       # True that current is in dict

            stop_ceas = time()

            if( (stop_ceas - start_ceas) >= turntime):
                alarm = 1
                return None

            for neighbor in self.neighbor_nodes(current, ants):

                stop_ceas = time()
                if( (stop_ceas - start_ceas) >= turntime):
                    alarm = 1
                    return None

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

    def do_turn(self, ants, start_ceas):
        directions = AIM
        destinations = []
        path = []
        ants.landmap()
        stop_ceas = 0
        nenorocire = 0
        delay = 0.40 * ants.turntime * 10**(-3) #convert from ms to s
        self.logger.info(delay)
        self.logger.info(ants.turntime)
        loopctr = 0

        if (self.hills == None):
            self.hills = ants.my_hills()
        for food in self.mancare:
            if food in ants.food_list:
                ants.food_list.remove(food)
        
        self.logger.info(ants.dead_list)
        
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow
            
            #Dupa a cata furnica se blocheaza totul?
            loopctr = loopctr + 1
            
            stop_ceas = time()
            if( (stop_ceas - start_ceas) >= delay ):
                nenorocire = 1
                break

            if self.paths.__contains__((a_row, a_col)):
                path = self.paths.pop((a_row, a_col))    # Get path of this ant
            else:
                closest_food = ants.closest_food(a_row, a_col)

                dist = maxint
                if closest_food != None:
                    dist = self.heuristic_cost_estimate((a_row, a_col),
                                                        closest_food, ants)
                if closest_food != None and dist <= DEFAULT_FOOD_DISTANCE:
                    stop_ceas = time()
                    
                    if( (stop_ceas - start_ceas) >= delay ):
                        nenorocire = 1
                        break
                    
                    path = self.Astar((a_row, a_col), closest_food, ants)
                    stop_ceas = time()
                    if( (stop_ceas - start_ceas) >= delay ):
                        nenorocire = 1
                        break

                    ants.food_list.remove(closest_food)
                    self.mancare.append(closest_food)

                elif dist >= DEFAULT_FOOD_DISTANCE:
                    unseen = ants.closest_unseen(a_row, a_col)
                    dist2 = self.heuristic_cost_estimate((a_row, a_col),
                                                        unseen, ants)
                    if ((a_row, a_col) in self.hills and
                        dist2 >= DEFAULT_HILL_DISTANCE):
                        if (drum_explorare == None):
                            stop_ceas = time()
                            if( (stop_ceas - start_ceas) >= delay ):
                                nenorocire = 1
                                break 
                            drum_explorare = self.Astar((a_row, a_col), unseen, ants)
                            stop_ceas = time()
                            if( (stop_ceas - start_ceas) >= delay ):
                                nenorocire = 1
                                break

                        else:
                            path = drum_explorare
                    else:
                        stop_ceas = time()
                        if( (stop_ceas - start_ceas) >= delay ):
                            nenorocire = 1
                            break

                        path = self.Astar((a_row, a_col), unseen, ants)

                        stop_ceas = time()
                        if( (stop_ceas - start_ceas) >= delay ):
                            nenorocire = 1
                            break
           
           #Daca a avut loc un timeout mutam toate furnicile nord
           #In loc de acest cod poate fi pusa mutarea random sau 
           #cautarea path-urilor cu BFS 
            if(nenorocire == 1):
                self.logger.info("Furnica sabotoare")
                self.logger.info(loopctr)

                destinations = []
                for a_row, a_col in ants.my_ants():
                # try all directions randomly until one is passable and not occupied
                    directions = (-1, 0)
                    for direction in directions:
                        (n_row, n_col) = ants.destination(a_row, a_col, direction)
                        if (not (n_row, n_col) in destinations and
                            ants.passable(n_row, n_col)):
                                ants.issue_order((a_row, a_col, direction))
                                destinations.append((n_row, n_col))
                                break
                        else:
                            destinations.append((a_row, a_col))


            #Ce era si inainte, doar ca nenorocirea (timeout-ul) se prespune
            # ca n-a avut loc
            if path != [] and nenorocire == 0:
                (n_row, n_col) = path.pop(0)        # Get next move.
                direction = ants.direction(a_row, a_col, n_row, n_col)

                if not (n_row, n_col) in destinations:
                    if len(path) == 1:
                        if path[0] in self.mancare:
                            self.mancare.remove(path[0])
                    if path != []:
                        # Update dict of paths with new coords for ant.
                        self.paths[(n_row, n_col)] = path;
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
        Ants.run(MyBot())
    except KeyboardInterrupt:
        print('ctrl-c, leaving ...')
