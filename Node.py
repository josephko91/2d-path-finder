# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 1
# The Oregon Trail
# Author: Joseph Ko
# This creates a Node class, 
# representing the node in search space
# -------------------------------------------------------
import numpy as np

class Node:
    def __init__(self, xy, h):
        self.coord = xy # coordinate of node 
        self.height = h # height of node
        self.cost = 0  # cumulated cost of node
        self.parent = 0 # parent of node
        self.id = 0 # unique ID of node
        self.heuristic = 0 # heuristic cost of node
        self.state_id = np.array2string(xy, precision=0, separator=',')