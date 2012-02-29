# Test A* in python interpreter / interactively

from heapq import heappush, heappop
from random import shuffle

# hardcodate
height = 30
width = 30

def heuristic_cost_estimate((row1, col1), (row2, col2)):
    '''Heuristic give estimated cost to goal'''
    row1 = row1 % height
    row2 = row2 % height
    col1 = col1 % width
    col2 = col2 % width
    d_col = min(abs(col1 - col2), width - abs(col1 - col2))
    d_row = min(abs(row1 - row2), height - abs(row1 - row2))
    return d_col + d_row

def neighbor_nodes(current):
    '''Return all neighbors for a given node'''
    l = []
    l.append(( (current[0] + 1) % height, current[1]))
    l.append(( (current[0] - 1) % height, current[1]))
    l.append((current[0], (current[1] + 1) % width))
    l.append((current[0], (current[1] - 1) % width))
    return l

def reconstruct_path(came_from, current_node):
    '''Construct path to target, from the beginning'''
    path = []
    while came_from[current_node] != None:
        path.insert(0, current_node)
        current_node = came_from[current_node]
    return path

def is_obstacle(coord, obstacles):
    try:
        x = obstacles[(coord[0], coord[1])]
        return True
    except KeyError:
        return False

def Astar(start, goal, obstacles):
    '''
    start, goal are tuples of the form (row, col);
    obstacles is a dictionary : (row, col) -> return Bool
    '''

    if ( is_obstacle(start, obstacles) or is_obstacle(goal, obstacles) ):
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
        _, current = heappop(heap)
        if current == goal:
            return reconstruct_path(came_from, goal)
        closedset[current] = True       # True that current is in dict

        for neighbor in neighbor_nodes(current):
            if (is_obstacle(neighbor, obstacles) or
            closedset.__contains__(neighbor)):
                continue
            if neighbor not in openset:
                openset += [neighbor]
                h_score = heuristic_cost_estimate(neighbor,goal)
                f_score = g_score + h_score
                heappush(heap, (f_score, neighbor))
                came_from[neighbor] = current
    return None
