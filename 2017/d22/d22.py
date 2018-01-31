# -*- coding: utf-8 -*-
"""
Advent of code
Day 22 - Part 1
"""

import os 
os.chdir("/Users/em/Documents/git-projects/adventofcode/2017/d22")

with open("input.txt", "r") as f:
    input = f.read()
    
#with open("test.txt", "r") as f:
#    input = f.read()

rows = input.split('\n')


def init_infected(rows):
    infected = []
    n_row = len(rows)
    n_col = len(rows[0])
    row_shift = (n_row-1)/2
    col_shift = (n_col-1)/2
    for i in range(n_row):
        for j in range(n_col):
            if (rows[i][j] == '#'):
                infected.append([i-row_shift,j-col_shift])
    return infected


def change_direction(d, change):
    """
    Change direction d depending on change value ('left' or 'right') 
    """
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

infected = init_infected(rows)
p = [0,0] # position
d = [-1,0] # direction

cnt = 0
rounds = 10000
for i in range(rounds):
    if p in infected:
        d = change_direction(d, 'right')
        infected.remove(p)
    else:
        d = change_direction(d, 'left')
        infected.append(list(p))
        cnt += 1
    p[0] += d[0]
    p[1] += d[1]

print(cnt)        
        





