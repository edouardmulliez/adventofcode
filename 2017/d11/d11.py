#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 23:37:20 2018

@author: em
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d11")

with open("input.txt", "r") as f:
    input = f.read()


directions = input.split(',')



def update_position(pos, direction):
    """
    Change pos depending on direction.
    """
    assert(direction in ['n', 's', 'nw', 'ne', 'sw', 'se'])
    
    if direction == 'n':
        pos[1] += 1
    elif direction == 's':
        pos[1] -= 1
    elif direction == 'ne':
        pos[0] += 1
        pos[1] += 0.5
    elif direction == 'nw':
        pos[0] -= 1
        pos[1] += 0.5    
    elif direction == 'se':
        pos[0] += 1
        pos[1] -= 0.5    
    elif direction == 'sw':
        pos[0] -= 1
        pos[1] -= 0.5
    else:
        raise ValueError('Incorrect direction')
    

def get_step_nb(pos):
    pos = [abs(p) for p in pos]
    step_nb = pos[0] + max(0, pos[1]- 0.5 * pos[0])
    return step_nb

# Part 1
pos = [0,0]
for direction in directions:
    update_position(pos, direction)

print(int(get_step_nb(pos)))

# Part 2
pos = [0,0]
max_step = 0
for direction in directions:
    update_position(pos, direction)
    max_step = max(max_step, get_step_nb(pos))
    
print(max_step)




    