#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 21:44:20 2018

@author: em
"""

import numpy as np
import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d21")

with open("input.txt", "r") as f:
    input = f.read()

lines = input.split('\n')

def from_string_to_array(s):
    """
    Convert string in a numpy array.
    """
    return np.array([[c for c in row] for row in s.split('/') ])

def from_array_to_string(a):
    return '/'.join([''.join(row) for row in a])

def get_all_array_variations(a):
    """
    Flip and rotate np array a to obtain a list with all variations of a.
    """
    flip_a = np.flip(a, 1)
    all_a = [a, flip_a]
    for i in range(3):
        all_a.append(np.rot90(a, i+1))
        all_a.append(np.rot90(flip_a, i+1))
    return all_a


def add_pattern(patterns, line):
    """
    Add elements to dictionary patterns corresponding to line. Keys of patterns 
    are input array as string, values are output arrays as numpy arrray.
    """
    el = line.split(' => ')
    keys = get_all_array_variations(from_string_to_array(el[0]))
    value = from_string_to_array(el[1])
    for k in keys:
        patterns[from_array_to_string(k)] = value


def enhance(a, patterns):
    """
    Returns an enhanced version of array, following rules in patterns.
    """
    return patterns[from_array_to_string(a)]


def update_grid(grid, patterns):
    
    # Compute new size and initialize new grid
    size = grid.shape[0]
    if size % 2 == 0:
        n = 2
    else:
        n = 3    
    size_2 = size * (n+1) / n
    g2 = np.chararray((size_2, size_2))
    
    for i in range(size/n):
        for j in range(size/n):            
            g2[i*(n+1):(i+1)*(n+1), j*(n+1):(j+1)*(n+1)] = \
                enhance(grid[i*n:(i+1)*n,j*n:(j+1)*n], patterns)
    return g2



patterns = {}
for line in lines:
    add_pattern(patterns, line)
    

assert(np.array_equal(update_grid(from_string_to_array('.#./..#/###'), patterns),
                      from_string_to_array('###./..#./.##./##..')))        


# Part 1
grid = from_string_to_array('.#./..#/###')

rounds = 5
for i in range(rounds):
    grid = update_grid(grid, patterns)
    
nb_on = (grid == '#').sum()
print(nb_on)

# Part 2
grid = from_string_to_array('.#./..#/###')
rounds = 18
for i in range(rounds):
    grid = update_grid(grid, patterns)
    
nb_on = (grid == '#').sum()
print(nb_on)


