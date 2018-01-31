#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Advent of code
Day 22 - Part 2
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d22")

with open("input.txt", "r") as f:
    input = f.read()
    
rows = input.split('\n')


def init_status(rows):
    """
    Returns a dictionary status where key are positions, values are status of 
    the nodes: O: clean, 1: weakened, 2: infected, 3: flagged
    """
    infected = {}
    n_row = len(rows)
    n_col = len(rows[0])
    row_shift = (n_row-1)/2
    col_shift = (n_col-1)/2
    for i in range(n_row):
        for j in range(n_col):
            if (rows[i][j] == '#'):
                infected[(i-row_shift,j-col_shift)] = 2
    return infected


def change_direction(d, change):
    """
    Change direction d depending on change value ('left', 'right' or 'back') 
    """
    if change=='back':
        return [-d[0], -d[1]]
    if (d[0]==0):
        if change=='left':
            return [-d[1],0]
        if change=='right':
            return [d[1],0]
    if (d[1]==0):
        if change=='left':
            return [0,d[0]]
        if change=='right':
            return [0,-d[0]]
    

assert(change_direction([0,1], 'left') == [-1,0])
assert(change_direction([0,1], 'right') == [1,0])
assert(change_direction([1,0], 'left') == [0,1])
assert(change_direction([1,0], 'right') == [0,-1]) 
assert(change_direction([1,0], 'back') == [-1,0]) 

status = init_status(rows)
p = [0,0] # position
d = [-1,0] # direction

cnt = 0
rounds = 10000000
for i in range(rounds):
    s = status.get((p[0],p[1]), 0)
    if s==0:
        # Clean
        d = change_direction(d, 'left')
    elif s==1:
        # weak
        cnt += 1
    elif s==2:
        # infected
        d = change_direction(d, 'right')
    elif s==3:
        # flagged
        d = change_direction(d, 'back')
    # update state and position
    status[(p[0],p[1])] = (s+1) % 4
    p[0] += d[0]
    p[1] += d[1]

print(cnt)        
