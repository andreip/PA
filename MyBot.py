#!/usr/bin/env python
from random import shuffle
from ants import *
from heapq import heappush, heappop
from logging import *
from logutils import *
from collections import deque
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
        self.drum_explorare = None
        self.hills = None
        self.trimit = 1;
        self.send_ants = []

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

    def reconstruct_path2(self, came_from, current_node):
        """! \brief Construieste drumul din parinte in parinte, pana la nodul
        initial (de la sfarsit spre inceput).

            \param current_node - nodul final, unde ajunge calea construita; e
            de forma unui tuplu (row, col).
            \param came_from - contine parintii nodurilor ce formeaza calea
            spre nodul final.
        """
        path = []
        while current_node != None:
            path.append(current_node[1])
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

    def bfs(self, foods, my_ants, ants):
        
        q = []
        came_from = {}
        closedset = {}
        openset = []
        count  = 0
        
        #pun in coada pozitia mancarii si mancarea.
        for food in foods:
            q.insert(0, (food, food, count))
            openset += [(food, food)]
            came_from [(food, food)]  = None
        
       # self.logger.info(q)
        while q != [] and my_ants != [] and foods !=[]:
            current = q.pop(0)
            #daca mancarea a ajuns la furnica
            #creez calea si sterg furnica si mancarea din liste.
            if current[1] in my_ants and current[0] in foods:
                path = self.reconstruct_path2(came_from, (current[0],
                current[1]))
                my_ants.remove(current[1])
                self.logger.info("oare?")
                foods.remove(current[0])
                self.logger.info("oare?")
                self.logger.info(current[0])
                self.logger.info(my_ants)
                self.logger.info(path)
                path.pop(0)
                self.paths[current[1]] = path
                self.send_ants.append(current[1])
                self.mancare.append(current[0])
            #daca manacarea a fost deja tintita o sterg din lista.
            if current[0] not in foods:
                self.logger.info("nu e ")
                continue
            if current[2] >= 15:
                self.logger.info("distanta prea mare")
                continue

            closedset[(current[0],current[1])] = True
            #iau toti vecinii punctului curent.
            
            
            for neighbor in self.neighbor_nodes(current[1], ants):
                #verific daca se poate realiza miscarea.
                if(not ants.passable(neighbor[0], neighbor[1]) or
                closedset.__contains__(neighbor) or 
                (ants.map[neighbor[0]][neighbor[1]] == UNSEEN)):
                    continue
                #verific daca mancarea asociata cu vecinul se mai afla in lista 
                
                if (current[0], neighbor) not in openset:
                    openset += [(current[0], neighbor)]
                    q.append((current[0], neighbor, current[2] + 1 ))
                    came_from[(current[0], neighbor)] = (current[0],
                    current[1])
                
        return None
    def do_turn(self, ants):
        directions = AIM
        destinations = []
        path = []
        ants.landmap()
        self.logger.info("Round")
        
        my_ants = ants.my_ants()
        foods = ants.food_list
        self.logger.info(my_ants)
        self.logger.info(self.send_ants)
        for ant in self.send_ants:
            if ant in my_ants:
                my_ants.remove(ant)
        for food in self.mancare:
            if food in foods:
                foods.remove(food)

        self.logger.info(my_ants)
        if my_ants != [] and foods!=[]:
            self.bfs(foods, my_ants, ants)
        self.logger.info(self.send_ants)
        
        self.logger.info(ants.dead_list)
        #ants_number = len(ants.my_ants())
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
            path = []
            if self.paths.__contains__((a_row, a_col)):
                path = self.paths.pop((a_row, a_col))    # Get path of this ant
                self.logger.info("mama")

            else:
                self.logger.info("end")
                directions = AIM.keys()
                self.logger.info("end")
                shuffle(directions)
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col,direction)
                    self.logger.info(direction)
                    if(not (n_row, n_col) in destinations ):
                        self.logger.info(direction)
                        ants.issue_order((a_row, a_col, direction))
                        self.logger.info("end")
                        destinations.append((n_row, n_col))
                        break
                    else:
                        destinations.append((a_row, a_col))
                        self.logger.info("end")
                    
            if path != []:
                (n_row, n_col) = path.pop(0)        # Get next move.
                direction = ants.direction(a_row, a_col, n_row, n_col)

                if not (n_row, n_col) in destinations:
                    if len(path) == 1:
                        if path[0] in self.mancare:
                            self.mancare.remove(path[0])
                    if path != []:
                        # Update dict of paths with new coords for ant.
                        self.paths[(n_row, n_col)] = path
                        self.send_ants.append((n_row, n_col))

                    if (a_row, a_col) in self.send_ants:
                        self.send_ants.remove((a_row, a_col))
                    ants.issue_order((a_row, a_col, direction[0]))
                    self.logger.info(direction[0])
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
