# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 1
# The Oregon Trail
# Author: Joseph Ko
# This is the main driver.
# -------------------------------------------------------

from collections import deque
from utility import print_to_output
import numpy as np
from search_algorithms import bfs, ucs, astar
import time

# parse input file
with open('input.txt', 'r') as input_file:
    algorithm = input_file.readline().rstrip() # 1st line: algorithm to run
    w, h = [int(x) for x in input_file.readline().rstrip().split()] # 2nd line: width and height of land map
    start = np.array(input_file.readline().rstrip().split(), dtype = int) # 3rd line: starting point
    max_height_delta = int(input_file.readline().rstrip()) # 4th line: maximum height difference allowed
    n = int(input_file.readline().rstrip()) # 5th line: number of settling sites
    target = np.empty((n, 2), dtype = int) # pre-allocate array
    for i in range(n): # next n lines: coordinates of settling sites
        coord = np.array(input_file.readline().rstrip().split(), dtype = int)
        target[i, ] = coord # append coordinates in order to np array
    grid = np.empty((h, w), dtype = int) # pre-allocate array
    for j in range(h): # next h lines: grid matrix
        row = np.array(input_file.readline().rstrip().split(), dtype = int)
        grid[j, ] = row

# test prints
print("======================== TEST CASE 50 ========================")
print('algorithm = ', algorithm)
print('width = ', w)
print('height = ', h)
print('start coordinate = ', start)
print('max allowed height change = ', max_height_delta)
print('# settling sites = ', n)
print('target coordinates = ', '\n', target)
print('grid = ', '\n', grid)
print('value at start: ', grid[start[1], start[0]])

start_time = time.time()
# Run algorithms and print results to output file
if algorithm == "BFS":
    with open('output.txt', 'w') as output:
        for i in range(n):
            result = bfs(grid, start, target[i, ], max_height_delta) 
            print_to_output(result, output, i, n)
elif algorithm == "UCS":
    with open('output.txt', 'w') as output:
        for i in range(n):
            result = ucs(grid, start, target[i, ], max_height_delta)
            print_to_output(result, output, i, n)
elif algorithm == "A*":
    with open('output.txt', 'w') as output:
        for i in range(n):
            result = astar(grid, start, target[i, ], max_height_delta)
            print_to_output(result, output, i, n)
end_time = time.time()
print('Algorithm run time = ', end_time - start_time, ' seconds')