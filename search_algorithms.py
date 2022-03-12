# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 1
# The Oregon Trail
# Author: Joseph Ko
# This module holds the different search algorithms
# -------------------------------------------------------

from collections import deque
from Node import Node
from utility import find_height, bound_check, height_check, simple_loop_check, loop_check, get_path, calc_unit_path_cost, sort_by_path_cost, find_mud_cost, calc_heuristic, astar_sort
import numpy as np
import time

# Breadth First Search (BFS)
def bfs(grid, start, target, max_height_delta):
    """ This function performs BFS on input data """
    # create start node
    w = grid.shape[1] # width of grid
    h = grid.shape[0] # height of grid
    neighbor_matrix = np.array([[1, -1], [1, 0], [1, 1], 
                                [0, -1], [0, 1],
                                [-1, -1], [-1, 0], [-1, 1]])
    start_height = find_height(grid, start)
    start_node = Node(start, start_height)
    node_id = 1 # initialize unique node id 
    start_node.id = node_id
    # add start_node to queue
    open_queue = deque()
    open_queue.append(start_node)
    closed = {} # initialize closed dictionary
    # loop until queue empty or target found
    loop_count = 1 # for testing 
    start_loop_time = time.time()
    #while True:
    while loop_count < 1001:
        #start_loop_time = time.time()
        if len(open_queue) == 0: # return fail if queue is empty
            result = 'FAIL'
            print('result: ', result) # test print
            print('cost: ', 2147483647) # for testing
            return result
        active_node = open_queue.popleft()
        #print('ACTIVE NODE: ', active_node.coord) #FOR TESTING
        if np.array_equal(active_node.coord, target): # return path when target is reached
            result = get_path(active_node, closed) # calls function to print full solution path
            print('result: ', result) # test print
            print('cost: ', len(result) - 1)
            return result
        for j in range(8): # loop through all 8 potential neighbors
            neighbor_coord = active_node.coord + neighbor_matrix[j]
            if bound_check(neighbor_coord, w, h): # boundary check
                neighbor_height = find_height(grid, neighbor_coord)
                if height_check(neighbor_height, active_node.height, max_height_delta): # height check
                    node_id += 1   
                    neighbor = Node(neighbor_coord, neighbor_height)
                    neighbor.id = node_id
                    neighbor.parent = active_node.id
                    open_queue, closed = loop_check(neighbor, closed, open_queue) # performs loop check and modifies open/closed as needed
        closed[active_node.id] = active_node # add node to closed dictionary
        #print('closed coord: ', closed[active_node.id].coord) #FOR TESTING 
        end_loop_time = time.time()
        # if loop_count % 1000 == 0: # for testing 
        #     print('still looping...just passed loop #', loop_count)
        #     print('time spent in loop #', loop_count, ': ', end_loop_time - start_loop_time, 'seconds')
        # loop_count += 1
        if loop_count % 10 == 0: # for testing 
            print('======================= loop #', loop_count, "=======================")
            print('Popped node ID: ', active_node.id)
            print('Popped node coord: ', active_node.coord)
            print('Parent of popped node: ', active_node.parent)
            print('elapsed time: ', end_loop_time - start_loop_time, 'seconds')
        loop_count += 1


# Uniform Cost Search (UCS)
def ucs(grid, start, target, max_height_delta):
    """ This function performs UCS on input data """
    # create start node
    w = grid.shape[1] # width of grid
    h = grid.shape[0] # height of grid
    neighbor_matrix = np.array([[1, -1], [1, 0], [1, 1], 
                                [0, -1], [0, 1],
                                [-1, -1], [-1, 0], [-1, 1]])
    start_height = find_height(grid, start)
    start_node = Node(start, start_height)
    node_id = 1 # initialize unique node id 
    start_node.id = node_id
    # add start_node to queue
    open_queue = deque()
    open_queue.append(start_node)
    closed = {} # initialize closed dictionary
    # loop until queue empty or target found
    loop_count = 1 # for testing 
    start_loop_time = time.time()
    #while True:
    while loop_count < 1001:
        #start_loop_time = time.time()
        if len(open_queue) == 0: # return fail if queue is empty
            result = 'FAIL'
            print('result: ', result) # test print
            print('cost: ', 2147483647) # for testing
            return result
        active_node = open_queue.popleft()
        #print('ACTIVE NODE: ', active_node.coord) #FOR TESTING
        if np.array_equal(active_node.coord, target): # return path when target is reached
            result = get_path(active_node, closed) # calls function to print full solution path
            print('result: ', result) # test print
            print('cost: ', active_node.cost) # for testing 
            return result
        for j in range(8): # loop through all 8 potential neighbors
            neighbor_coord = active_node.coord + neighbor_matrix[j]
            unit_path_cost = calc_unit_path_cost(neighbor_matrix[j])
            if bound_check(neighbor_coord, w, h): # boundary check
                neighbor_height = find_height(grid, neighbor_coord)
                if height_check(neighbor_height, active_node.height, max_height_delta): # height check
                    node_id += 1   
                    neighbor = Node(neighbor_coord, neighbor_height)
                    neighbor.id = node_id
                    neighbor.parent = active_node.id
                    neighbor.cost = active_node.cost + unit_path_cost # cumulative path cost
                    open_queue, closed = loop_check(neighbor, closed, open_queue) # performs loop check and modifies open/closed as needed
        closed[active_node.id] = active_node # add node to closed dictionary
        open_queue = sort_by_path_cost(open_queue) # sort open queue
        #print('closed coord: ', closed[active_node.id].coord) #FOR TESTING 
        end_loop_time = time.time()
        if loop_count % 10 == 0: # for testing 
            print('======================= loop #', loop_count, "=======================")
            print('Popped node ID: ', active_node.id)
            print('Popped node coord: ', active_node.coord)
            print('Parent of popped node: ', active_node.parent)
            print('elapsed time: ', end_loop_time - start_loop_time, 'seconds')
        loop_count += 1

# A* search (astar)
def astar(grid, start, target, max_height_delta):
    """ This function performs A* on input data """
    # create start node
    w = grid.shape[1] # width of grid
    h = grid.shape[0] # height of grid
    neighbor_matrix = np.array([[1, -1], [1, 0], [1, 1], 
                                [0, -1], [0, 1],
                                [-1, -1], [-1, 0], [-1, 1]])
    start_height = find_height(grid, start)
    start_node = Node(start, start_height)
    node_id = 1 # initialize unique node id 
    start_node.id = node_id
    # add start_node to queue
    open_queue = deque()
    open_queue.append(start_node)
    closed = {} # initialize closed dictionary
    loop_count = 1 # for testing 
    # loop until queue empty or target found
    start_loop_time = time.time()
    #while True:
    while loop_count < 1001:
    #for i in range(2): # testing 
        #start_loop_time = time.time()
        if len(open_queue) == 0: # return fail if queue is empty
            result = 'FAIL'
            print('result: ', result) # test print
            print('cost: ', 2147483647) # for testing
            return result
        active_node = open_queue.popleft()
        #print('ACTIVE NODE: ', active_node.coord) #FOR TESTING
        if np.array_equal(active_node.coord, target): # return path when target is reached
            result = get_path(active_node, closed) # calls function to print full solution path
            print('result: ', result) # test print
            print('cost: ', active_node.cost) # for testing 
            return result
        for j in range(8): # loop through all 8 potential neighbors
            neighbor_coord = active_node.coord + neighbor_matrix[j]
            unit_path_cost = calc_unit_path_cost(neighbor_matrix[j])
            if bound_check(neighbor_coord, w, h): # boundary check
                neighbor_height = find_height(grid, neighbor_coord)
                mud_cost = find_mud_cost(grid, neighbor_coord, neighbor_height)
                #print('mud cost: ', neighbor_coord, mud_cost) #testing
                if height_check(neighbor_height, active_node.height, max_height_delta): # height check
                    height_change = abs(neighbor_height - active_node.height)
                    node_id += 1   
                    neighbor = Node(neighbor_coord, neighbor_height)
                    neighbor.id = node_id
                    neighbor.parent = active_node.id
                    neighbor.cost = active_node.cost + unit_path_cost + mud_cost + height_change # cumulative path cost
                    neighbor.heuristic = calc_heuristic(neighbor_coord, target)
                    open_queue, closed = loop_check(neighbor, closed, open_queue) # performs loop check and modifies open/closed as needed
        closed[active_node.id] = active_node # add node to closed dictionary
        open_queue = astar_sort(open_queue) # sort open queue
        end_loop_time = time.time()
        # if loop_count % 1000 == 0: # for testing 
        #     print('still looping...just passed loop #', loop_count)
        #     print('time spent in loop #', loop_count, ': ', end_loop_time - start_loop_time, 'seconds')
        # loop_count += 1
        if loop_count % 10 == 0: # for testing 
            print('======================= loop #', loop_count, "=======================")
            print('Popped node ID: ', active_node.id)
            print('Popped node coord: ', active_node.coord)
            print('Parent of popped node: ', active_node.parent)
            print('elapsed time: ', end_loop_time - start_loop_time, 'seconds')
        loop_count += 1
        #print('closed coord: ', closed[active_node.id].coord) #FOR TESTING 