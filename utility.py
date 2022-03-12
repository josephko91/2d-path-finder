# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 1
# The Oregon Trail
# Author: Joseph Ko
# This module holds utility functions
# -------------------------------------------------------
import numpy as np
from collections import deque
from Node import Node

# Function to find height of cell
def find_height(grid, coord):
    """ This function outputs the height in a cell """
    x = coord[0]
    y = coord[1]
    if (grid[y, x] < 0):
        return abs(grid[y, x])
    else: 
        return 0

# Check if coord is in bound of grid 
def bound_check(coord, w, h):
    """ Checks if coord is within grid """
    if (0 <= coord[1] < h) and (0 <= coord[0] < w):
        return True
    else: 
        return False

# Check if elevation change condition is satisfied
def height_check(h1, h2, max_height_delta):
    """ Checks if elevation change condition """
    if (abs(h1 - h2) <= max_height_delta):
        return True
    else:
        return False

# Simple loop detector
def simple_loop_check(neighbor, closed):
    """ Checks if neighbor is in closed list """
    for key in closed:
        if (np.array_equal(closed[key].coord, neighbor)):
            return False
    return True

# Loop detector (more sophisticated version)
def loop_check(neighbor, closed, open_queue):
    """ Checks if there is a loop, returns open and closed list """
    open_list = list(open_queue) # populate list of open node (i.e. nodes in queue)
    open_matches = 0
    closed_matches = 0
    # check for open node with same state
    for node in open_list:
        if (np.array_equal(node.coord, neighbor.coord)): 
            open_matches += 1
            if neighbor.cost < node.cost:
                open_list.remove(node) # delete existing 
                open_list.append(neighbor) # append neighbor
            break
    # check for closed node with same state
    for key in closed: 
        node = closed[key]
        if (np.array_equal(node.coord, neighbor.coord)): 
            closed_matches += 1
            if neighbor.cost < node.cost:
                del closed[node.id] # delete existing 
                open_list.append(neighbor) # append neighbor
            break
    # if there are no matches found at all in open or closed
    if (open_matches + closed_matches == 0):
        open_list.append(neighbor) # append neighbor
    open_queue = deque(open_list)
    return open_queue, closed

# Function print solution path
def get_path(end, closed):
    """ This function prints the path from start to target """
    path_q= deque()
    path = []
    node = end # start at target and trace back
    path_q.append(node) # append target node to initialize
    while (node.parent != 0): # backtracking
        node = closed[node.parent] # set parent to node
        path_q.append(node) # append to right side of queue
    while path_q: # convert to list
        popped_node = path_q.pop()
        path.append(popped_node.coord)
    return path # return list of nodes

# Function returns unit path cost
def calc_unit_path_cost(unit_coord):
    """ returns 14 if diagonal, 10 if not diagonal """
    if (sum(np.abs(unit_coord)) == 2): # sum of magnitudes of coords == 2 if diagonal
        return 14
    else: 
        return 10

# Function sorts a queue by path cost
def sort_by_path_cost(open_queue): 
    """ sort queue by path cost """
    open_list = list(open_queue)
    open_queue = deque(sorted(open_list, key = lambda node: node.cost))
    return open_queue

# Function that prints results to output file
def print_to_output(result, output, i, n):
    """ prints result from algorithm to output file """
    if i == (n - 1):
        if type(result) == str:
            print(result, file = output, end = '')
        else:
            for i in range(len(result)):
                if i == (len(result) - 1):
                    print(result[i][0], ',', result[i][1], file = output, sep = '', end = '')
                else:
                    print(result[i][0], ',', result[i][1], file = output, sep = '', end = ' ')
    else: 
        if type(result) == str:
            print(result, file = output)
        else:
            for i in range(len(result)):
                if i == (len(result) - 1):
                    print(result[i][0], ',', result[i][1], file = output, sep = '')
                else:
                    print(result[i][0], ',', result[i][1], file = output, sep = '', end = ' ')

# Function that calculates the mud cost of moving into a cell
def find_mud_cost(grid, neighbor_coord, neighbor_height):
    """ returns cost of muddiness in cell you travel into """
    x = neighbor_coord[0]
    y = neighbor_coord[1]
    if neighbor_height > 0:
        return 0
    else:
        return grid[y, x]

# Function that calculates heuristic cost from node n to target
def calc_heuristic(neighbor_coord, target):
    """ Returns hueristic cost. Chebyshev distance used here. """
    x1 = neighbor_coord[0]
    x2 = target[0]
    y1 = neighbor_coord[1]
    y2 = target[1]
    return max(abs(y2 - y1), abs(x2 - x1)) # Chebyshev distance

# Function sorts a queue by path cost
def astar_sort(open_queue): 
    """ sort queue by path cost + heuristic """
    open_list = list(open_queue)
    open_queue = deque(sorted(open_list, key = lambda node: (node.cost + node.heuristic, node.heuristic)))
    return open_queue