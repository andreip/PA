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

class Ant:
    def __init__(self):
        self.dist = 0
        self.source = None
        self.position = None
        self.next_position = None
        self.moved = False

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
        self.turn_number = 0

        self.destinations = []


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

    def move_ant(self, next_coord, ant, ants):
        (n_row, n_col) = next_coord        # Get next move.
        (a_row, a_col) = ant
        direction = ants.direction(a_row, a_col, n_row, n_col)

        if not (n_row, n_col) in self.destinations:
            ants.issue_order((a_row, a_col, direction[0]))
            self.destinations.append((n_row, n_col))
            ants.land_count[n_row][n_col] +=1
        else:
            self.destinations.append((a_row, a_col))
            ants.land_count[a_row][a_col] += 1

    def bfs(self, foods, my_ants, ants):
        q = []
        came_from = {}
        closedset = {}
        openset = {}
        count  = 0
        creat_ants = []
        #pun in coada pozitia mancarii si mancarea.
        for food in foods:
            ant = Ant()
            ant.source = food
            ant.position = food
            ant.dist = 0
            #self.logger.info("Formez furnici")
            q.insert(0, ant)
            openset[(food, food)] = True
        while q != [] and my_ants != [] and foods !=[]:
            current = q.pop(0)
            #daca mancarea a ajuns la furnica
            #creez calea si sterg furnica si mancarea din liste.
            if current.position in my_ants and current.source in foods:
                #self.logger.info("rebuild")
                #path = self.reconstruct_path2(came_from, (current.source,
                #current.position))
                #just move
                self.move_ant(current.next_position, current.position, ants)
                my_ants.remove(current.position)
                foods.remove(current.source)
                self.send_ants.append(current.position)
                self.mancare.append(current.source)

                #ant = Ant()
                #ant.position = current.position
                #ant.moved = True
                creat_ants.append(current)
            if current.source not in foods:
                continue
            if current.dist >= 10:
                continue
            closedset[(current.source,current.position)] = True
            # iau toti vecinii punctului curent.
            for neighbor in self.neighbor_nodes(current.position, ants):
                # verific daca se poate realiza miscarea.
                if(not ants.passable(neighbor[0], neighbor[1]) or
                   closedset.__contains__(neighbor)):
                    continue
                #verific daca mancarea asociata cu vecinul se mai afla in lista 
                if (current.source, neighbor) not in openset:
                    openset[(current.source, neighbor)] = True
                    ant = Ant()
                    ant.source = current.source
                    ant.position = neighbor
                    ant.next_position = current.position
                    ant.moved = True
                    ant.dist = current.dist + 1
                    q.append(ant)

        for ant in my_ants:
            creat_ant = Ant()
            creat_ant.source = ant
            creat_ants.append(creat_ant)

        return creat_ants
        #return None 

    def initTurn(self, ants):
        # save the ants list for this given turn
        ants.my_ants_list = ants.my_ants()
        #ants.landmap()
        self.turn_number += 1

        self.logger.info("turn #" + str(self.turn_number) + ":")
        self.logger.info("my_ants: " + str(ants.my_ants_list))

    def do_turn(self, ants):
        path = []
        directions = AIM.keys()
        self.logger.info("Round")
        self.initTurn(ants)
        self.logger.info("initTurn exit")
        border = ants.find_cluster_border()
        my_ants = ants.my_ants_list

        foods = ants.food_list
        #self.logger.info("food: " + str(ants.food_list))
        #for ant in self.send_ants:
        #    if ant in my_ants:
        #        my_ants.remove(ant)
        #for food in self.mancare:
        #    if food in foods:
        #        foods.remove(food)
        #for ant in ants.my_ants():
        #    creat_ant = Ant()
        #    creat_ant.source = ant
        #    my_ants.append(creat_ant)

        new_ants = []
        if my_ants != []:# and foods != []:
            new_ants = self.bfs(foods, my_ants, ants)
        #ants_number = len(ants.my_ants())
        #self.logger.info("new ants: " + str(new_ants))

        for ant in new_ants:
            if not ant.moved:
                next_coord = None
                path = []
                if ant.source in ants.my_hills() and border != []:
                        self.logger.info("doare")
                        self.logger.info(ant.source)
                        next_coord = ants.get_next_coord(ant.source, border)
                        self.logger.info("----> next")
                        self.logger.info(next_coord)
                 
                if next_coord != None:
                    path = next_coord

                elif self.paths.__contains__(ant.source):
                    path = self.paths.pop(ant.source)
                else:
                    minim = 1000
                    next_node = None
                    if not ants.is_visited(ant.source):
                        ants.set_visited(ant.source)
                        closest_my =  ants.closest_my_hill(ant.source[0], ant.source[1])
                        self.logger.info("Centru cluster:")
                        self.logger.info(ants.get_center(ant.source))
                         
                        path_square = self.Astar(closest_my, ant.source, ants) 
                        ants.set_path(ant.source , path_square)
                        ants.set_source(ant.source, closest_my)
                    for neighbor in self.neighbor_nodes(ant.source, ants):
                        if ants.land_count[neighbor[0]][neighbor[1]] < minim and ants.passable(neighbor[0], neighbor[1]):
                            minim = ants.land_count[neighbor[0]][neighbor[1]]
                            next_node = neighbor


                    self.move_ant(next_node, ant.source, ants)
                self.logger.info("here")
                if path != []:
                    (n_row, n_col) = path.pop(0)        # Get next move.
                    direction = ants.direction(ant.source[0], ant.source[1], n_row, n_col)

                    if not (n_row, n_col) in destinations:
                        if path != []:
                            # Update dict of paths with new coords for ant.
                            self.paths[(n_row, n_col)] = path;
                        ants.issue_order((ant.source[0], ant.source[1], direction[0]))
                        destinations.append((n_row, n_col))
                    else:
                        destinations.append(ant.source)


               
               
               
               
                    """
                self.logger.info(ant.moved)
                (a_row, a_col) = ant.source
                directions = AIM.keys()
                shuffle(directions)
                self.logger.info("shuffle")
                for direction in directions:
                    self.logger.info("here")
                    (n_row, n_col) = ants.destination(a_row, a_col,direction)
                    
                    self.logger.info    if(not (n_row, n_col) in self.destinations) and ants.passable(n_row, n_col):

                        self.logger.info(direction)
                        ants.issue_order((a_row, a_col, direction))
                        self.destinations.append((n_row, n_col))
                        break
                    else:
                        self.destinations.append((a_row, a_col))
                    """ 
        self.destinations = []
        """
        for a_row, a_col in ants.my_ants():
            # If ant has a path to follow, follow it.
            path = []

            if self.paths.__contains__((a_row, a_col)):
                path = self.paths.pop((a_row, a_col))    # Get path of this ant

            else:
                directions = AIM.keys()
                shuffle(directions)
                for direction in directions:
                    (n_row, n_col) = ants.destination(a_row, a_col,direction)
                    self.logger.info(direction)
                    if(not (n_row, n_col) in destinations ):
                        self.logger.info(direction)
                        ants.issue_order((a_row, a_col, direction))
                        destinations.append((n_row, n_col))
                        break
                    else:
                        destinations.append((a_row, a_col))
                    
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
                    destinations.append((n_row, n_col))
                else:
                    destinations.append((a_row, a_col))
        """
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
