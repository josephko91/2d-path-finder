# -------------------------------------------------------
# CSCI 561, Spring 2021
# Homework 1
# The Oregon Trail
# Author: Joseph Ko
# Randomly generate arrays of numbers and print to file
# -------------------------------------------------------
from collections import deque
from Node import Node
import numpy as np
import utility as util
from random import seed, randint

lower_bound = -1
upper_bound = 5
randnums = np.random.randint(lower_bound, upper_bound, size = (5, 5))
with open('random_numbers.txt', 'w') as output:
    for line in randnums:
        for i in range(len(line)):
            if i == (len(line) - 1):
                print(line[i], file = output, sep = '')
            else:
                print(line[i], file = output, sep = '', end = ' ')